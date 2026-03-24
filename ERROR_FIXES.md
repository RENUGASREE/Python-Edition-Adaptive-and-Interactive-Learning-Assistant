# Error Fixes Summary

## Issues Fixed

### 1. **400 Bad Request on `/api/user-progress/` ✅**
**Problem:** Frontend was sending unsupported fields (`timeSpent`, `hintsUsed`) that don't exist in the backend UserProgress model, causing validation failures.

**Solution:**
- **Backend** ([core/serializers.py](core/serializers.py#L399)): Updated `UserProgressSerializer` to accept `userId` as writable field (auto-populated from request user)
- **Backend** ([core/views.py](core/views.py#L671)): Modified `UserProgressViewSet.create()` to auto-populate `user_id` from authenticated user instead of relying on client
- **Frontend** ([client/src/hooks/use-progress.ts](client/src/hooks/use-progress.ts#L45)): Removed `timeSpent` and `hintsUsed` fields from API payload; now only sends: `lessonId`, `completed`, `score`, `lastCode`, `completedAt`

### 2. **net::ERR_INTERNET_DISCONNECTED (Google Fonts) ✅**
**Problem:** When offline or with poor connection, Google Fonts CDN fails to load, but no fallback fonts were defined.

**Solution:**
- Added inline `<style>` block in [client/index.html](client/index.html#L10) with system font fallbacks
- Added `onerror` handler to Google Fonts `<link>` tag to gracefully log failures
- Now uses system fonts (Segoe UI, Roboto, Courier New) when Google Fonts unavailable

### 3. **Input() Function in Python Console ✅**
**Status:** Backend implementation is already correct and properly configured!

**How it works:**
- When you enter code like `int(input("enter a value:"))` in the code editor
- The input you type in the "**Input (for code using input() function)**" textarea is passed to Python via stdin
- Backend executes: `subprocess.run(..., input=user_input_text, ...)`

**If still not working, check:**
1. Make sure you're entering input in the textarea labeled "Input (for code using input() function)"
2. The input field must be visible on the page (in LessonView and Challenges components)
3. Browser console should show no errors when clicking "Run Code"

---

## Files Modified

| File | Change | Impact |
|------|--------|--------|
| [backend/core/serializers.py](backend/core/serializers.py#L399) | Updated `UserProgressSerializer` | Fixes 400 Bad Request errors |
| [backend/core/views.py](backend/core/views.py#L671) | Modified `UserProgressViewSet.create()` | Auto-populates user from auth session |
| [client/src/hooks/use-progress.ts](client/src/hooks/use-progress.ts#L45) | Removed unsupported fields | Prevents API validation failures |
| [client/index.html](client/index.html#L10) | Added fallback fonts + error handler | Works offline with degraded fonts |

---

## Testing Instructions

### Test 1: User Progress Update
1. Complete a lesson/challenge
2. Open browser DevTools (F12) → Network tab
3. Look for POST `/api/user-progress/` request
4. Verify response status is **200 OK** (not 400)

### Test 2: Python Input Function
1. Write code like: `name = input("Enter your name: ")`
2. Enter text in the "Input" textarea
3. Click "Run Code"
4. Check console output section for the input being processed

### Test 3: Offline Mode
1. In DevTools → Network → throttle to "Offline"
2. Refresh the page
3. Page should still render with fallback fonts
4. No red X marks on `<link>` tags in console

---

## Additional Notes
- The React DevTools warning is informational - no action needed, but you can install the extension for better debugging
- All changes are backward compatible
- No database migrations needed

