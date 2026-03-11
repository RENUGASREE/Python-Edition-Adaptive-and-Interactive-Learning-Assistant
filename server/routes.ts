import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { api } from "@shared/routes";
import { db } from "./db";
import { modules, lessons, quizzes, questions, challenges, users } from "@shared/schema";
import { z } from "zod";
import { exec } from "child_process";
import fs from "fs";
import path from "path";
import util from "util";
import { authStorage } from "./replit_integrations/auth/storage";
import crypto from "crypto";

const execAsync = util.promisify(exec);

export async function registerRoutes(
  httpServer: Server,
  app: Express
): Promise<Server> {
  // Integrations
  app.get("/healthz", (_req, res) => {
    res.status(200).json({ status: "ok" });
  });

  // API Routes
  app.get("/api/auth/user", async (req, res) => {
    const userId = (req.session as any)?.userId as string | undefined;
    if (!userId) return res.status(401).json({ message: "Unauthorized" });
    const user = await authStorage.getUser(userId);
    if (!user) return res.status(401).json({ message: "Unauthorized" });
    return res.json(user);
  });

  const registerSchema = z.object({
    email: z.string().email(),
    password: z.string().min(6),
    firstName: z.string().optional(),
    lastName: z.string().optional(),
  });
  const loginSchema = z.object({
    email: z.string().email(),
    password: z.string(),
  });
  function hashPassword(pw: string) {
    const salt = crypto.randomBytes(16).toString("hex");
    const key = crypto.scryptSync(pw, salt, 64).toString("hex");
    return `s:${salt}:${key}`;
  }
  function verifyPassword(pw: string, stored: string) {
    const parts = stored.split(":");
    if (parts.length !== 3) return false;
    const salt = parts[1];
    const key = crypto.scryptSync(pw, salt, 64).toString("hex");
    return key === parts[2];
  }
  app.post("/api/auth/register", async (req, res) => {
    const input = registerSchema.parse(req.body);
    const existing = await db.select().from(users).where(eq(users.email, input.email)).limit(1);
    if (existing.length > 0) return res.status(409).json({ message: "User already exists" });
    const user = await authStorage.upsertUser({
      email: input.email,
      firstName: input.firstName,
      lastName: input.lastName,
      passwordHash: hashPassword(input.password),
      updatedAt: new Date(),
    });
    (req.session as any).userId = user.id;
    res.json(user);
  });
  app.post("/api/auth/login", async (req, res) => {
    const input = loginSchema.parse(req.body);
    const found = await db.select().from(users).where(eq(users.email, input.email)).limit(1);
    if (found.length === 0 || !found[0].passwordHash || !verifyPassword(input.password, found[0].passwordHash)) {
      return res.status(401).json({ message: "Invalid credentials" });
    }
    (req.session as any).userId = found[0].id;
    res.json(found[0]);
  });

  // Logout and destroy session
  app.get("/api/logout", (req, res) => {
    req.session.destroy(() => {
      res.clearCookie("connect.sid");
      res.redirect("/");
    });
  });

  app.get(api.modules.list.path, async (req, res) => {
    const modules = await storage.getModules();
    res.json(modules);
  });

  app.get(api.modules.get.path, async (req, res) => {
    const module = await storage.getModule(Number(req.params.id));
    if (!module) return res.status(404).json({ message: "Module not found" });
    
    // Get lessons for this module (simple query for now)
    const allLessons = await db.select().from(lessons).where(eq(lessons.moduleId, module.id)).orderBy(asc(lessons.order));
    
    res.json({ ...module, lessons: allLessons });
  });

  app.get(api.lessons.get.path, async (req, res) => {
    const lesson = await storage.getLessonWithDetails(Number(req.params.id));
    if (!lesson) return res.status(404).json({ message: "Lesson not found" });
    res.json(lesson);
  });

  console.log("Registering route:", api.challenges.run.path);
  app.post(api.challenges.run.path, async (req, res) => {
    console.log("Received request for /api/challenges/:id/run");
    try {
      const { code, testCases = [] } = req.body;
      const challengeId = Number(req.params.id);
      const [challenge] = await db.select().from(challenges).where(eq(challenges.id, challengeId)).limit(1);
      const effectiveTestCases = testCases.length > 0 ? testCases : (challenge?.testCases || []);
      
      const fileName = `temp_${Date.now()}.py`;
      const tmpDir = path.join(process.cwd(), 'tmp');
      await fs.promises.mkdir(tmpDir, { recursive: true });
      const filePath = path.join(tmpDir, fileName);
      console.log("Executing Python file at:", filePath);
      
      await fs.promises.writeFile(filePath, code);

      try {
        // Determine the correct Python command based on OS
        const pythonCommand = process.platform === 'win32' ? 'python' : 'python3';
        console.log(`Using Python command: ${pythonCommand}`);
        
        const { stdout, stderr } = await execAsync(`${pythonCommand} "${filePath}"`, { timeout: 5000 });
        console.log(`Python stdout: ${stdout}`);
        console.log(`Python stderr: ${stderr}`);
        
        let allPassed = true;
        if (effectiveTestCases.length > 0) {
          allPassed = effectiveTestCases.every((tc: any) => {
            const expected = tc.expected?.trim();
            const actual = stdout?.trim();
            return actual === expected;
          });
        }

        res.json({
          output: stdout || stderr,
          error: stderr || null,
          passed: allPassed && !stderr,
        });
      } catch (error: any) {
        console.error(`Python execution error:`, error);
        res.json({
          output: error.stdout || "",
          error: error.stderr || error.message || "Failed to execute Python script",
          passed: false,
        });
      } finally {
        try {
          await fs.promises.unlink(filePath);
        } catch (e) { /* ignore */ }
      }
    } catch (error) {
      console.error("Error in /api/challenges/:id/run:", error);
      res.status(500).json({ message: "Execution failed" });
    }
  });

  app.get(api.progress.get.path, async (req, res) => {
    const userId = (req.session as any)?.userId as string | undefined;
    if (!userId) return res.status(401).json({ message: "Unauthorized" });
    const progress = await storage.getUserProgress(userId);
    res.json(progress);
  });

  app.post(api.progress.update.path, async (req, res) => {
    const userId = (req.session as any)?.userId as string | undefined;
    if (!userId) return res.status(401).json({ message: "Unauthorized" });
    const input = api.progress.update.input.parse(req.body);
    const updated = await storage.updateUserProgress(userId, input);
    res.json(updated);
  });

  // Placeholder for creating a new conversation
  app.post("/api/conversations", async (req, res) => {
    // For now, just return a dummy conversation ID
    res.json({ id: 1 });
  });

  // Seed Data
  try {
    await seedDatabase();
  } catch (err) {
    console.error("Seeding failed:", err);
  }

  return httpServer;
}

// Helpers
import { eq, asc } from "drizzle-orm";

async function seedDatabase() {
  console.log("Seeding or updating curriculum...");

  const placementQuestions = [
    {
      text: "What will this code print?\n\nprint(\"Hello\" + \"Python\")",
      options: [
        { text: "HelloPython", correct: true },
        { text: "Hello Python", correct: false },
        { text: "Hello+Python", correct: false },
        { text: "Error", correct: false },
      ],
      points: 5,
    },
    {
      text: "Which data type is produced by: 3 / 2",
      options: [
        { text: "int", correct: false },
        { text: "float", correct: true },
        { text: "str", correct: false },
        { text: "bool", correct: false },
      ],
      points: 5,
    },
    {
      text: "What does this evaluate to?\n\n5 > 3 and 2 < 1",
      options: [
        { text: "True", correct: false },
        { text: "False", correct: true },
        { text: "5", correct: false },
        { text: "1", correct: false },
      ],
      points: 5,
    },
    {
      text: "Which loop is best when you know the number of iterations?",
      options: [
        { text: "for loop", correct: true },
        { text: "while loop", correct: false },
        { text: "if statement", correct: false },
        { text: "try/except", correct: false },
      ],
      points: 5,
    },
    {
      text: "What is the output?\n\nnums = [2, 4, 6]\nprint(len(nums))",
      options: [
        { text: "2", correct: false },
        { text: "3", correct: true },
        { text: "6", correct: false },
        { text: "Error", correct: false },
      ],
      points: 5,
    },
    {
      text: "Which structure stores key-value pairs?",
      options: [
        { text: "list", correct: false },
        { text: "tuple", correct: false },
        { text: "set", correct: false },
        { text: "dictionary", correct: true },
      ],
      points: 5,
    },
    {
      text: "What does this print?\n\nfor i in range(1, 4):\n    print(i)",
      options: [
        { text: "1 2 3", correct: true },
        { text: "0 1 2 3", correct: false },
        { text: "1 2 3 4", correct: false },
        { text: "1 3", correct: false },
      ],
      points: 10,
    },
    {
      text: "Which function returns a value without printing it?",
      options: [
        { text: "print()", correct: false },
        { text: "input()", correct: false },
        { text: "return", correct: true },
        { text: "type()", correct: false },
      ],
      points: 10,
    },
    {
      text: "What is the result of: [x * 2 for x in [1, 2, 3]]",
      options: [
        { text: "[2, 4, 6]", correct: true },
        { text: "[1, 2, 3, 2]", correct: false },
        { text: "[1, 4, 9]", correct: false },
        { text: "Error", correct: false },
      ],
      points: 10,
    },
    {
      text: "What is a common use of a lambda function?",
      options: [
        { text: "Define a short anonymous function", correct: true },
        { text: "Create a class", correct: false },
        { text: "Import a module", correct: false },
        { text: "Handle file I/O", correct: false },
      ],
      points: 10,
    },
    {
      text: "Which statement best describes recursion?",
      options: [
        { text: "A loop that never ends", correct: false },
        { text: "A function calling itself", correct: true },
        { text: "A variable changing type", correct: false },
        { text: "A list inside a tuple", correct: false },
      ],
      points: 10,
    },
    {
      text: "What does this output?\n\ndef f(n):\n    if n == 0:\n        return 0\n    return n + f(n - 1)\n\nprint(f(3))",
      options: [
        { text: "3", correct: false },
        { text: "6", correct: true },
        { text: "9", correct: false },
        { text: "Error", correct: false },
      ],
      points: 15,
    },
  ];

  const curriculum = [
    {
      title: "Introduction to Python",
      description: "Learn the foundations of Python with clear examples and practice.",
      lessons: [
        {
          title: "Hello World",
          slug: "hello-world",
          duration: 10,
          content: `Python reads your code from top to bottom and executes it line by line.\n\n## Why this lesson matters\nPrinting text is the simplest way to confirm your environment is working and to understand how Python outputs results.\n\n## Example\n\`\`\`python\nprint("Hello, Python!")\n\`\`\`\n\n## Try it\nChange the message inside print and run the code again.\n\n## Personalization\nYour placement quiz and lesson progress build a personalized path. Finish the quiz to unlock the right starting point for you.`,
          challenge: {
            description: "Print exactly: Hello, Python!",
            initialCode: "print(\"\")",
            solutionCode: "print(\"Hello, Python!\")",
            expectedOutput: "Hello, Python!",
          },
        },
        {
          title: "Variables",
          slug: "variables",
          duration: 15,
          content: `Variables store values so you can reuse them later.\n\n## Key idea\nA variable is a label that points to data.\n\n## Example\n\`\`\`python\nname = "Asha"\nprint("Hello, " + name)\n\`\`\`\n\n## Try it\nReplace the name with your own and see the output change.`,
          challenge: {
            description: "Create a variable named name with value Asha and print Hello, Asha",
            initialCode: "name = \"\"\nprint(\"Hello, \" + name)",
            solutionCode: "name = \"Asha\"\nprint(\"Hello, \" + name)",
            expectedOutput: "Hello, Asha",
          },
        },
        {
          title: "Data Types",
          slug: "data-types",
          duration: 15,
          content: `Python has several basic types: strings, integers, floats, and booleans.\n\n## Examples\n\`\`\`python\nage = 18\nprice = 19.99\nactive = True\ntext = "Python"\nprint(type(price))\n\`\`\`\n\n## Try it\nChange the values and observe the types.`,
          challenge: {
            description: "Compute the average of 10 and 20 and print the result",
            initialCode: "a = 10\nb = 20\nprint((a + b) / 2)",
            solutionCode: "a = 10\nb = 20\nprint((a + b) / 2)",
            expectedOutput: "15.0",
          },
        },
        {
          title: "User Input",
          slug: "user-input",
          duration: 15,
          content: `input() lets users type data that your program can use.\n\n## Example\n\`\`\`python\nname = input(\"Enter your name: \")\nprint(\"Welcome, \" + name)\n\`\`\`\n\n## Tip\nWhen practicing here, we use preset values so tests can verify your output.\n\n## Try it\nReplace input with a variable value to simulate user data.`,
          challenge: {
            description: "Set age to 18 and print Age: 18",
            initialCode: "age = 18\nprint(\"Age: \" + str(age))",
            solutionCode: "age = 18\nprint(\"Age: \" + str(age))",
            expectedOutput: "Age: 18",
          },
        },
        {
          title: "Basic Math",
          slug: "basic-math",
          duration: 15,
          content: `Python supports +, -, *, /, //, %, and ** for math.\n\n## Example\n\`\`\`python\nprint((5 + 3) * 2)\n\`\`\`\n\n## Try it\nExperiment with division and power.`,
          challenge: {
            description: "Print the result of (5 + 3) * 2",
            initialCode: "print((5 + 3) * 2)",
            solutionCode: "print((5 + 3) * 2)",
            expectedOutput: "16",
          },
        },
      ],
    },
    {
      title: "Control Flow",
      description: "Make your programs choose different paths with conditions.",
      lessons: [
        {
          title: "If Statements",
          slug: "if-statements",
          duration: 20,
          content: `If statements let code run only when a condition is true.\n\n## Example\n\`\`\`python\nscore = 85\nif score >= 60:\n    print("Pass")\n\`\`\`\n\n## Try it\nChange the score and see how the output changes.`,
          challenge: {
            description: "If score is at least 60, print Pass",
            initialCode: "score = 85\nif score >= 60:\n    print(\"Pass\")",
            solutionCode: "score = 85\nif score >= 60:\n    print(\"Pass\")",
            expectedOutput: "Pass",
          },
        },
        {
          title: "Else & Elif",
          slug: "else-elif",
          duration: 20,
          content: `elif lets you check multiple conditions in order.\n\n## Example\n\`\`\`python\ntemp = 30\nif temp > 30:\n    print("Hot")\nelif temp >= 20:\n    print("Warm")\nelse:\n    print("Cold")\n\`\`\`\n\n## Try it\nAdjust the temperature and test each branch.`,
          challenge: {
            description: "Print Hot if temp > 29, Warm if temp >= 20, otherwise Cold",
            initialCode: "temp = 30\nif temp > 29:\n    print(\"Hot\")\nelif temp >= 20:\n    print(\"Warm\")\nelse:\n    print(\"Cold\")",
            solutionCode: "temp = 30\nif temp > 29:\n    print(\"Hot\")\nelif temp >= 20:\n    print(\"Warm\")\nelse:\n    print(\"Cold\")",
            expectedOutput: "Hot",
          },
        },
        {
          title: "Comparison Operators",
          slug: "comparison",
          duration: 15,
          content: `Use ==, !=, <, <=, >, >= to compare values.\n\n## Example\n\`\`\`python\nprint(7 < 10)\n\`\`\`\n\n## Try it\nCompare different values and observe True or False.`,
          challenge: {
            description: "Print the result of 7 < 10",
            initialCode: "print(7 < 10)",
            solutionCode: "print(7 < 10)",
            expectedOutput: "True",
          },
        },
        {
          title: "Logical Operators",
          slug: "logical",
          duration: 15,
          content: `Combine conditions with and, or, and not.\n\n## Example\n\`\`\`python\nage = 20\nhas_id = True\nif age >= 18 and has_id:\n    print("Allowed")\n\`\`\`\n\n## Try it\nFlip the booleans to see the effect.`,
          challenge: {
            description: "Print Allowed if age >= 18 and has_id is True",
            initialCode: "age = 20\nhas_id = True\nif age >= 18 and has_id:\n    print(\"Allowed\")",
            solutionCode: "age = 20\nhas_id = True\nif age >= 18 and has_id:\n    print(\"Allowed\")",
            expectedOutput: "Allowed",
          },
        },
        {
          title: "Nested Ifs",
          slug: "nested-if",
          duration: 20,
          content: `Nested ifs let you check a condition inside another condition.\n\n## Example\n\`\`\`python\nnum = 8\nif num > 0:\n    if num % 2 == 0:\n        print("Positive even")\n\`\`\`\n\n## Try it\nChange the number and check the output.`,
          challenge: {
            description: "Print Positive even when num is positive and even",
            initialCode: "num = 8\nif num > 0:\n    if num % 2 == 0:\n        print(\"Positive even\")",
            solutionCode: "num = 8\nif num > 0:\n    if num % 2 == 0:\n        print(\"Positive even\")",
            expectedOutput: "Positive even",
          },
        },
      ],
    },
    {
      title: "Loops & Iteration",
      description: "Repeat actions to automate tasks.",
      lessons: [
        {
          title: "For Loops",
          slug: "for-loops",
          duration: 20,
          content: `For loops iterate over items in a sequence.\n\n## Example\n\`\`\`python\nfor i in [1, 2, 3]:\n    print(i)\n\`\`\`\n\n## Try it\nUse a list of your own numbers.`,
          challenge: {
            description: "Print numbers 1 to 5, each on its own line",
            initialCode: "for i in range(1, 6):\n    print(i)",
            solutionCode: "for i in range(1, 6):\n    print(i)",
            expectedOutput: "1\n2\n3\n4\n5",
          },
        },
        {
          title: "Range Function",
          slug: "range",
          duration: 15,
          content: `range(start, stop) generates a sequence of numbers.\n\n## Example\n\`\`\`python\nfor i in range(1, 4):\n    print(i * i)\n\`\`\`\n\n## Try it\nChange the stop value and observe the output.`,
          challenge: {
            description: "Print squares of 1, 2, and 3 on separate lines",
            initialCode: "for i in range(1, 4):\n    print(i * i)",
            solutionCode: "for i in range(1, 4):\n    print(i * i)",
            expectedOutput: "1\n4\n9",
          },
        },
        {
          title: "While Loops",
          slug: "while-loops",
          duration: 20,
          content: `While loops repeat as long as a condition stays true.\n\n## Example\n\`\`\`python\ncount = 3\nwhile count > 0:\n    print(count)\n    count -= 1\n\`\`\`\n\n## Try it\nStart from a different number.`,
          challenge: {
            description: "Count down from 3 to 1",
            initialCode: "count = 3\nwhile count > 0:\n    print(count)\n    count -= 1",
            solutionCode: "count = 3\nwhile count > 0:\n    print(count)\n    count -= 1",
            expectedOutput: "3\n2\n1",
          },
        },
        {
          title: "Break & Continue",
          slug: "break-continue",
          duration: 15,
          content: `break stops a loop early, continue skips to the next iteration.\n\n## Example\n\`\`\`python\nfor i in range(1, 6):\n    if i == 3:\n        continue\n    print(i)\n\`\`\`\n\n## Try it\nReplace continue with break and compare.`,
          challenge: {
            description: "Print 1, 2, 4, 5 using continue to skip 3",
            initialCode: "for i in range(1, 6):\n    if i == 3:\n        continue\n    print(i)",
            solutionCode: "for i in range(1, 6):\n    if i == 3:\n        continue\n    print(i)",
            expectedOutput: "1\n2\n4\n5",
          },
        },
        {
          title: "Nested Loops",
          slug: "nested-loops",
          duration: 25,
          content: `Nested loops repeat one loop inside another.\n\n## Example\n\`\`\`python\nfor i in range(1, 3):\n    for j in range(1, 3):\n        print(i * j)\n\`\`\`\n\n## Try it\nPrint results in a small table format.`,
          challenge: {
            description: "Print a 2x2 multiplication table: 1 2 then 2 4",
            initialCode: "for i in range(1, 3):\n    row = []\n    for j in range(1, 3):\n        row.append(str(i * j))\n    print(\" \".join(row))",
            solutionCode: "for i in range(1, 3):\n    row = []\n    for j in range(1, 3):\n        row.append(str(i * j))\n    print(\" \".join(row))",
            expectedOutput: "1 2\n2 4",
          },
        },
      ],
    },
    {
      title: "Data Structures",
      description: "Work with lists, tuples, dictionaries, and sets.",
      lessons: [
        {
          title: "Lists Basics",
          slug: "lists-basics",
          duration: 20,
          content: `Lists store ordered collections you can change.\n\n## Example\n\`\`\`python\nnums = [1, 2, 3]\nprint(sum(nums))\n\`\`\`\n\n## Try it\nAdd more numbers and recalculate.`,
          challenge: {
            description: "Create a list [1, 2, 3] and print the sum",
            initialCode: "nums = [1, 2, 3]\nprint(sum(nums))",
            solutionCode: "nums = [1, 2, 3]\nprint(sum(nums))",
            expectedOutput: "6",
          },
        },
        {
          title: "List Methods",
          slug: "list-methods",
          duration: 20,
          content: `Lists have methods like append, pop, and insert.\n\n## Example\n\`\`\`python\nletters = [\"a\", \"b\"]\nletters.append(\"c\")\nprint(letters[-1])\n\`\`\`\n\n## Try it\nUse pop() to remove the last item.`,
          challenge: {
            description: "Append c to the list and print the last element",
            initialCode: "letters = [\"a\", \"b\"]\nletters.append(\"c\")\nprint(letters[-1])",
            solutionCode: "letters = [\"a\", \"b\"]\nletters.append(\"c\")\nprint(letters[-1])",
            expectedOutput: "c",
          },
        },
        {
          title: "Tuples",
          slug: "tuples",
          duration: 15,
          content: `Tuples are ordered but cannot be changed.\n\n## Example\n\`\`\`python\ncoords = (10, 20)\nprint(coords[1])\n\`\`\`\n\n## Try it\nAccess the first element and print it.`,
          challenge: {
            description: "Print the second element from the tuple (10, 20)",
            initialCode: "coords = (10, 20)\nprint(coords[1])",
            solutionCode: "coords = (10, 20)\nprint(coords[1])",
            expectedOutput: "20",
          },
        },
        {
          title: "Dictionaries",
          slug: "dictionaries",
          duration: 25,
          content: `Dictionaries store key-value pairs.\n\n## Example\n\`\`\`python\nstudent = {\"name\": \"Sam\", \"age\": 14}\nprint(student[\"name\"], student[\"age\"])\n\`\`\`\n\n## Try it\nAdd a new key and print it.`,
          challenge: {
            description: "Print name and age from the dictionary",
            initialCode: "student = {\"name\": \"Sam\", \"age\": 14}\nprint(student[\"name\"], student[\"age\"])",
            solutionCode: "student = {\"name\": \"Sam\", \"age\": 14}\nprint(student[\"name\"], student[\"age\"])",
            expectedOutput: "Sam 14",
          },
        },
        {
          title: "Sets",
          slug: "sets",
          duration: 20,
          content: `Sets store unique values and remove duplicates.\n\n## Example\n\`\`\`python\nvalues = {1, 2, 2, 3}\nprint(len(values))\n\`\`\`\n\n## Try it\nAdd a new value and print the length.`,
          challenge: {
            description: "Create a set {1, 2, 2, 3} and print its length",
            initialCode: "values = {1, 2, 2, 3}\nprint(len(values))",
            solutionCode: "values = {1, 2, 2, 3}\nprint(len(values))",
            expectedOutput: "3",
          },
        },
      ],
    },
    {
      title: "Functions & Scope",
      description: "Build reusable and well-structured code.",
      lessons: [
        {
          title: "Defining Functions",
          slug: "def-functions",
          duration: 25,
          content: `Functions group instructions so you can call them many times.\n\n## Example\n\`\`\`python\ndef greet():\n    return \"Hello\"\n\nprint(greet())\n\`\`\`\n\n## Try it\nReturn a different message.`,
          challenge: {
            description: "Define greet() that returns Hello and print it",
            initialCode: "def greet():\n    return \"Hello\"\n\nprint(greet())",
            solutionCode: "def greet():\n    return \"Hello\"\n\nprint(greet())",
            expectedOutput: "Hello",
          },
        },
        {
          title: "Parameters",
          slug: "parameters",
          duration: 20,
          content: `Parameters let you pass data into a function.\n\n## Example\n\`\`\`python\ndef add(a, b):\n    return a + b\n\nprint(add(3, 4))\n\`\`\`\n\n## Try it\nCall the function with different numbers.`,
          challenge: {
            description: "Create add(a, b) and print add(3, 4)",
            initialCode: "def add(a, b):\n    return a + b\n\nprint(add(3, 4))",
            solutionCode: "def add(a, b):\n    return a + b\n\nprint(add(3, 4))",
            expectedOutput: "7",
          },
        },
        {
          title: "Return Values",
          slug: "return",
          duration: 20,
          content: `return sends a value back to the caller.\n\n## Example\n\`\`\`python\ndef area(r):\n    return 3.14 * r * r\n\nprint(area(2))\n\`\`\`\n\n## Try it\nReturn area for a different radius.`,
          challenge: {
            description: "Define area(r) and print area(2)",
            initialCode: "def area(r):\n    return 3.14 * r * r\n\nprint(area(2))",
            solutionCode: "def area(r):\n    return 3.14 * r * r\n\nprint(area(2))",
            expectedOutput: "12.56",
          },
        },
        {
          title: "Global vs Local Scope",
          slug: "scope",
          duration: 20,
          content: `Variables inside a function are local unless declared global.\n\n## Example\n\`\`\`python\nx = 5\n\ndef show():\n    x = 2\n    print(x)\n\nshow()\nprint(x)\n\`\`\`\n\n## Try it\nRename the variable and observe the output.`,
          challenge: {
            description: "Print local x then global x",
            initialCode: "x = 5\n\ndef show():\n    x = 2\n    print(x)\n\nshow()\nprint(x)",
            solutionCode: "x = 5\n\ndef show():\n    x = 2\n    print(x)\n\nshow()\nprint(x)",
            expectedOutput: "2\n5",
          },
        },
        {
          title: "Lambda Functions",
          slug: "lambda",
          duration: 25,
          content: `Lambda functions are short anonymous functions.\n\n## Example\n\`\`\`python\nadd = lambda a, b: a + b\nprint(add(2, 3))\n\`\`\`\n\n## Try it\nCreate a lambda to double a number.`,
          challenge: {
            description: "Create a lambda that doubles 6 and print the result",
            initialCode: "double = lambda x: x * 2\nprint(double(6))",
            solutionCode: "double = lambda x: x * 2\nprint(double(6))",
            expectedOutput: "12",
          },
        },
      ],
    },
  ];

  const existingModules = await db.select().from(modules).orderBy(asc(modules.order));
  const modulesByOrder = new Map(existingModules.map((m) => [m.order, m]));

  for (let i = 0; i < curriculum.length; i++) {
    const modData = curriculum[i];
    const order = i + 1;
    let mod = modulesByOrder.get(order);
    if (mod) {
      await db.update(modules).set({
        title: modData.title,
        description: modData.description,
        order,
      }).where(eq(modules.id, mod.id));
    } else {
      const inserted = await db.insert(modules).values({
        title: modData.title,
        description: modData.description,
        order,
      }).returning();
      mod = inserted[0];
    }

    const existingLessons = await db.select().from(lessons).where(eq(lessons.moduleId, mod.id)).orderBy(asc(lessons.order));
    const lessonsByOrder = new Map(existingLessons.map((l) => [l.order, l]));

    for (let j = 0; j < modData.lessons.length; j++) {
      const lessonData = modData.lessons[j];
      const lessonOrder = j + 1;
      const content = `# ${lessonData.title}\n\n${lessonData.content}`;
      let lesson = lessonsByOrder.get(lessonOrder);
      if (lesson) {
        await db.update(lessons).set({
          title: lessonData.title,
          slug: lessonData.slug,
          content,
          order: lessonOrder,
          duration: lessonData.duration,
        }).where(eq(lessons.id, lesson.id));
      } else {
        const insertedLesson = await db.insert(lessons).values({
          moduleId: mod.id,
          title: lessonData.title,
          slug: lessonData.slug,
          content,
          order: lessonOrder,
          duration: lessonData.duration,
        }).returning();
        lesson = insertedLesson[0];
      }

      const challengePayload = {
        lessonId: lesson.id,
        title: `${lessonData.title} Challenge`,
        description: lessonData.challenge.description,
        initialCode: lessonData.challenge.initialCode,
        solutionCode: lessonData.challenge.solutionCode,
        testCases: [{ input: "", expected: lessonData.challenge.expectedOutput }],
        points: 20,
      };

      const existingChallenge = await db.select().from(challenges).where(eq(challenges.lessonId, lesson.id)).limit(1);
      if (existingChallenge.length > 0) {
        await db.update(challenges).set(challengePayload).where(eq(challenges.id, existingChallenge[0].id));
      } else {
        await db.insert(challenges).values(challengePayload);
      }

      if (i === 0 && j === 0) {
        const existingQuiz = await db.select().from(quizzes).where(eq(quizzes.lessonId, lesson.id)).limit(1);
        let quizId: number;
        if (existingQuiz.length > 0) {
          quizId = existingQuiz[0].id;
          await db.update(quizzes).set({ title: "Placement Quiz" }).where(eq(quizzes.id, quizId));
        } else {
          const insertedQuiz = await db.insert(quizzes).values({
            lessonId: lesson.id,
            title: "Placement Quiz",
          }).returning();
          quizId = insertedQuiz[0].id;
        }

        await db.delete(questions).where(eq(questions.quizId, quizId));
        await db.insert(questions).values(placementQuestions.map((q) => ({
          quizId,
          text: q.text,
          type: "multiple_choice",
          options: q.options,
          points: q.points,
        })));
      }
    }
  }

  console.log("Curriculum seeded or updated successfully!");
}
