import { drizzle } from "drizzle-orm/node-postgres";
import pg from "pg";
import * as schema from "@shared/schema";

const { Pool } = pg;

if (!process.env.DATABASE_URL) {
  throw new Error(
    "DATABASE_URL must be set. Did you forget to provision a database?",
  );
}

// Debug logging for DB connection (safe masking)
const dbUrl = process.env.DATABASE_URL;
const maskedUrl = dbUrl.replace(/:[^:@]*@/, ":****@");
const sslFlag =
  process.env.NODE_ENV === "production" ||
  process.env.DATABASE_SSL === "true" ||
  /[?&](sslmode=require|ssl=true)(?:[&]|$)/i.test(dbUrl);
console.log(`[DB] Connecting to database at: ${maskedUrl}`);
console.log(`[DB] SSL Mode: ${sslFlag ? "Enabled (rejectUnauthorized: false)" : "Disabled"}`);

try {
  const url = new URL(dbUrl);
  if (!url.password && process.env.NODE_ENV === "production") {
     console.warn("[DB] WARNING: No password found in DATABASE_URL. Connection may fail in production if not using .pgpass.");
  }
} catch (e) {
  console.warn("[DB] WARNING: Could not parse DATABASE_URL to check for password.");
}

export const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: sslFlag ? { rejectUnauthorized: false } : undefined,
  max: 5,
});
export const db = drizzle(pool, { schema });
