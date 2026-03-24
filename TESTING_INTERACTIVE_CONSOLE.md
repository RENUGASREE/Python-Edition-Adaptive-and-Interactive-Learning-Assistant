# Testing the Interactive Console - Quick Start

## ✅ What's Done

All code changes are **complete and ready to test**:

- ✅ Backend: Fixed field mapping (`userId`)
- ✅ Frontend: Interactive console component created
- ✅ Logic: Input detection and step-by-step input handling implemented
- ✅ Both Pages: LessonView and Challenges updated
- ✅ Styling: Color-coded output (yellow/green/red)

---

## 🚀 How to Test

### **Step 1: Restart the Frontend**

Open a terminal and run:

```bash
cd client
npm run dev
```

You should see: `VITE v5.x.x ready in xxx ms`

### **Step 2: Make Sure Backend is Running**

In another terminal:

```bash
cd backend
python manage.py runserver
```

You should see: `Starting development server at http://127.0.0.1:8000/`

### **Step 3: Open the App**

Go to: http://localhost:5173

---

## 🧪 Test Cases

### **Test 1: Go to Lessons**

1. Navigate to **Lessons** section
2. Find the **"Sum of Two"** challenge (or any lesson with code containing `input()`)
3. Look at the starting code or write your own:

```python
a = int(input("enter first number: "))
b = int(input("enter second number: "))
print("sum:", a + b)
```

4. Click **"Run Code"**

### **Expected Behavior**

**Step 1:** Console should show:
```
enter first number:
» [input field appears here]
```

The text should be **yellow**, and the cursor should be **in the input field**.

**Step 2:** Type `5` and press Enter (or click Send)

Console should now show:
```
enter first number:
5
enter second number:
» [input field appears here]
```

The `5` should be in **green** (user input), and the cursor should move back to the input field.

**Step 3:** Type `10` and press Enter

Console should now show:
```
enter first number:
5
enter second number:
10
sum: 15
```

The `sum: 15` should be in **green** (program output).

---

### **Test 2: Challenge with Tests**

1. Go to **Challenges** section
2. Find or create a challenge with input:

```python
x = int(input("value: "))
y = x * 2
print(y)
```

With input `5`, expected output should be `10`

3. Click **"Run Code"**
4. Follow same flow as Test 1

---

### **Test 3: Code Without Input**

1. Write or select code with **no** `input()` calls:

```python
print("Hello, World!")
```

2. Click **"Run Code"**

**Expected:** Code should execute **immediately** (no interactive mode), and you should see `Hello, World!` in the console in green.

---

### **Test 4: Error Handling**

1. Write code that expects a number but receives text:

```python
x = int(input("number: "))
print(x + 10)
```

2. Click **"Run Code"**
3. When prompted for input, type `abc` (not a number)
4. Press Enter

**Expected:** Error message should appear in **red** in the console:
```
number:
abc
ValueError: invalid literal for int() with base 10: 'abc'
```

---

## 📋 Checklist

As you test, check off these items:

- [ ] Prompts appear in **yellow**
- [ ] Input field appears and auto-focuses
- [ ] User input appears in **green** after Enter
- [ ] Next prompt appears correctly
- [ ] Final output appears in **green**
- [ ] Tests pass notification appears (if applicable)
- [ ] No console errors in browser DevTools
- [ ] Confetti animation works on lesson completion
- [ ] "Next Lesson" button appears after completion
- [ ] Non-input code still runs directly (no interactive mode)
- [ ] Errors appear in **red**

---

## 🐛 Troubleshooting

### **Issue: Input field doesn't appear**

**Solution:** 
- Make sure the code contains `input()` calls
- Check browser DevTools (F12) for JavaScript errors
- Restart the frontend with `npm run dev`

### **Issue: Console doesn't show colors**

**Solution:**
- Check that Tailwind CSS is loaded (inspect element styles)
- Look for any CSS errors in browser DevTools

### **Issue: Code executes but doesn't wait for input**

**Solution:**
- Open DevTools Console tab
- Look for error messages
- Check that `getInputCount()` is detecting inputs correctly

### **Issue: "Next Lesson" button doesn't appear**

**Solution:**
- Make sure tests passed (check output)
- Look for error in browser DevTools
- Check that userId field is being sent correctly (Network tab)

---

## 📊 Visual Reference

### **Interactive Mode Console**

```
┌────────────────────────────────────────────┐
│ Interactive Console                        │
├────────────────────────────────────────────┤
│ enter first number:   ← YELLOW PROMPT      │
│ 5                     ← GREEN USER INPUT   │
│ enter second number:  ← YELLOW PROMPT      │
│ 10                    ← GREEN USER INPUT   │
│ sum: 15               ← GREEN OUTPUT       │
│                                            │
│ ┌──────────────────────┐ ┌─────────┐      │
│ │ »  [cursor here]     │ │  Send   │      │
│ └──────────────────────┘ └─────────┘      │
└────────────────────────────────────────────┘
```

### **Non-Interactive Mode Console**

```
┌────────────────────────────────────────────┐
│ Hello, World!                              │
└────────────────────────────────────────────┘
```

---

## 🎯 Success Criteria

All tests pass when:

1. ✅ Prompts appear as yellow text
2. ✅ Input field appears below prompts
3. ✅ User inputs are captured and shown in green
4. ✅ Each input submission shows immediately in console
5. ✅ Final program output appears after all inputs
6. ✅ No errors in browser console
7. ✅ Lesson completion works (tests pass, confetti appears, next button shows)

---

## 📞 If Something Goes Wrong

1. **Check the browser DevTools (F12)**
   - Look in the "Console" tab for errors
   - Look in the "Network" tab to see if API calls are working

2. **Check the backend terminal**
   - Look for 400 errors or exceptions
   - Should see POST requests to `/api/user-progress/` with proper data

3. **Check the file changes**
   - Make sure all files were modified (see file list below)
   - Run `npm run build` to check for TypeScript errors

---

## 📝 Files Modified

| File | Change |
|------|--------|
| `client/src/components/TerminalConsole.tsx` | Added `InteractiveConsole` component |
| `client/src/pages/LessonView.tsx` | Added interactive mode logic |
| `client/src/pages/Challenges.tsx` | Added interactive mode logic |
| `client/src/lib/interactive-console.ts` | NEW - Utility functions |
| `backend/core/views.py` | Fixed userId field mapping (line 676) |

---

## ✨ Ready to Test!

Your interactive console is fully implemented and ready to use. Just restart the frontend and you'll see the magic happen! 🚀

---

**Need help?** Check the browser console for errors, or review the INTERACTIVE_CONSOLE_GUIDE.md for technical details.
