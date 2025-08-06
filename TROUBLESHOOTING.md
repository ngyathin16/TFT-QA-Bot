# TFT QA Bot - Troubleshooting Guide

## 🚨 **Common Issues and Solutions**

### **Problem: Chatbot returns generic responses instead of specific champion names**

**Symptoms:**
- Responses like "3-cost champion" instead of "Ahri, Caitlyn, Darius..."
- Responses like "5 1-cost champions" instead of listing actual names
- Inconsistent behavior between API tests and UI

**Root Causes:**
1. **Python bytecode cache** (`__pycache__` directory)
2. **Next.js build cache** (`.next` directory)
3. **Browser caching** of API responses
4. **Server not restarted** after code changes

## 🔧 **Solutions**

### **Quick Fix (Recommended)**
Use the provided restart scripts:

**Windows (PowerShell):**
```powershell
.\restart_server.ps1
```

**Windows (Command Prompt):**
```cmd
restart_server.bat
```

### **Manual Fix**
1. **Stop all servers:**
   ```bash
   # Stop Python processes
   taskkill /F /IM python.exe
   
   # Stop Node.js processes (if needed)
   taskkill /F /IM node.exe
   ```

2. **Clear all caches:**
   ```bash
   # Remove Python cache
   Remove-Item -Recurse -Force __pycache__
   
   # Remove Next.js cache
   Remove-Item -Recurse -Force .next
   ```

3. **Restart servers:**
   ```bash
   # Start backend (in one terminal)
   python backend_server.py
   
   # Start frontend (in another terminal)
   npm run dev
   ```

4. **Clear browser cache:**
   - Press `Ctrl+Shift+R` (hard refresh)
   - Or open Developer Tools → Network → Disable cache

## 🎯 **Best Practices**

### **When to Restart Servers**
- ✅ After making code changes
- ✅ When the chatbot gives incorrect responses
- ✅ When you see generic responses instead of specific data
- ✅ After pulling new code from Git

### **When NOT to Restart**
- ❌ Just for testing different questions
- ❌ When the chatbot is working correctly
- ❌ For simple UI changes (just refresh the page)

### **Testing Workflow**
1. **Make code changes**
2. **Run restart script** (`restart_server.ps1`)
3. **Wait 10-15 seconds** for servers to start
4. **Open http://localhost:3000**
5. **Test with hard refresh** (`Ctrl+Shift+R`)
6. **Test API directly** if UI seems wrong:
   ```bash
   Invoke-WebRequest -Uri "http://localhost:5000/api/chat" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"message": "List all 2-cost champions"}'
   ```

## 🔍 **Diagnostic Commands**

### **Check if servers are running:**
```bash
# Check Python processes
tasklist | findstr python

# Check Node.js processes
tasklist | findstr node
```

### **Test API directly:**
```bash
# Test 1-cost champions
Invoke-WebRequest -Uri "http://localhost:5000/api/chat" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"message": "List all 1-cost champions"}'

# Test 2-cost champions
Invoke-WebRequest -Uri "http://localhost:5000/api/chat" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"message": "List all 2-cost champions"}'

# Test 3-cost champions
Invoke-WebRequest -Uri "http://localhost:5000/api/chat" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"message": "List all 3-cost champions"}'
```

### **Expected API Responses:**
- **1-cost**: Should list 14 champions (Aatrox, Ezreal, Garen, etc.)
- **2-cost**: Should list 13 champions (Janna, Jhin, Kai'Sa, etc.)
- **3-cost**: Should list 16 champions (Ahri, Caitlyn, Darius, etc.)
- **4-cost**: Should list 13 champions (Akali, Ashe, Jarvan IV, etc.)
- **5-cost**: Should list 9 champions (Braum, Gwen, Lee Sin, etc.)

## 🚀 **Prevention Tips**

1. **Always use restart scripts** after code changes
2. **Clear browser cache** with `Ctrl+Shift+R`
3. **Test API directly** if UI seems wrong
4. **Check server logs** for error messages
5. **Verify `.env` file** has correct API key

## 📞 **Still Having Issues?**

If the problem persists after following these steps:

1. **Check server logs** for error messages
2. **Verify API key** in `.env` file
3. **Test with different browsers** (Chrome, Firefox, Edge)
4. **Check if ports are available** (5000 for backend, 3000 for frontend)
5. **Restart your computer** if all else fails

---

**Last Updated**: August 6, 2025 