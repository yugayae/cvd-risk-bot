# 🚀 Quick Start Guide - CVD Risk Analytics

## 📋 Prerequisites

- Python 3.8+
- Node.js (optional, for advanced bundling)
- Modern web browser
- FastAPI backend running

---

## 🏃 Getting Started (5 minutes)

### Step 1: Start the Backend

```bash
# Navigate to project root
cd c:\HomeWork\Medical\CVD_risk_Cat_Boost\cvd-risk-api

# Install dependencies (if not already done)
pip install -r requirements.txt

# Start the backend server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Step 2: Open the Frontend

#### Option A: Direct Browser
```bash
# Navigate to frontend directory
cd frontend

# Open in browser (double-click or copy to address bar)
file:///c:/HomeWork/Medical/CVD_risk_Cat_Boost/cvd-risk-api/frontend/index.html
```

#### Option B: Local Web Server (Recommended)
```bash
# From frontend directory
python -m http.server 3000

# Open browser to:
http://localhost:3000
```

---

## ✨ Features to Test

### 1. Language Switching
- Click the language dropdown in top-right
- Select English, Русский, or 한국어
- UI updates instantly ✅

### 2. Form Filling
Fill in sample data:
- Age: 45
- Gender: Male
- Systolic BP: 120
- Diastolic BP: 80
- Cholesterol: Normal
- Glucose: Normal
- BMI: 24.5
- Smoking: No
- Alcohol: No
- Physical Activity: Yes

### 3. Risk Calculation
- Click "Рассчитать риск" (Calculate Risk) button
- Wait for API response (backend processes the data)
- See results appear with animations

### 4. View Results
- Risk percentage with color-coded badge
- Patient profile radar chart
- Contributing factors bar chart
- AI recommendations in selected language

---

## 🔌 API Integration Test

### Test Backend Connection

```javascript
// Open browser console (F12)
// Paste this code:

fetch('http://localhost:8000/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        age_years: 45,
        ap_hi: 120,
        ap_lo: 80,
        cholesterol: 1,
        gluc: 1,
        bmi: 24.5,
        active: 1,
        smoke: 0,
        alco: 0,
        gender: 1,
        ui_language: 'en'
    })
})
.then(r => r.json())
.then(d => console.log('✅ Success:', d))
.catch(e => console.error('❌ Error:', e))
```

Expected output:
```json
{
  "risk_probability": 0.12,
  "risk_category": "low",
  "clinical_explanation": [...]
}
```

---

## 🐛 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **"Cannot connect to backend"** | Ensure backend is running on `localhost:8000`. Check with `curl http://localhost:8000/` |
| **Charts not appearing** | Open browser console (F12) and check for errors. Ensure Chart.js CDN is accessible |
| **Form submission hangs** | Check network tab (F12). Verify backend is responding with `/predict` endpoint |
| **Language not changing** | Clear browser cache (Ctrl+Shift+Del) and reload page |
| **CORS errors in console** | Backend CORS is already configured. If still failing, check `app/main.py` |

---

## 📂 File Structure

```
frontend/
├── index.html                 # Main application (open this!)
├── js/
│   ├── i18n.js               # Translations (EN, RU, KR)
│   ├── config.js             # Settings & thresholds
│   ├── api-service.js        # Backend API connector
│   └── dashboard.js          # Main controller
├── FRONTEND_SETUP.md         # Detailed documentation
├── INTEGRATION_GUIDE.md      # Integration overview
└── verify-setup.py           # Verification script
```

---

## 🎯 Testing Scenarios

### Scenario 1: Low Risk Patient
```
Age: 35, Male, BP: 110/70, Cholesterol: Normal, No smoking
→ Should show 🟢 Low Risk
```

### Scenario 2: Moderate Risk Patient
```
Age: 55, Male, BP: 140/90, Cholesterol: Above Normal, Smoker
→ Should show 🟠 Moderate Risk
```

### Scenario 3: High Risk Patient
```
Age: 65, Male, BP: 160/100, Cholesterol: High, Smoker
→ Should show 🔴 High Risk
```

---

## 📊 Monitoring Backend

### Check Backend Health
```bash
curl http://localhost:8000/
# Response: {"status":"ok"}
```

### Get Model Metrics
```bash
curl http://localhost:8000/metrics
# Shows performance metrics
```

### Backend Logs
Watch the terminal where you started uvicorn:
```
INFO:     GET / HTTP/1.1" 200 OK
INFO:     POST /predict HTTP/1.1" 200 OK
```

---

## 🔐 Security Notes

- ✅ CORS configured for `localhost` development
- ✅ Client-side validation for user inputs
- ✅ Server-side validation enforced
- ✅ No sensitive data stored in localStorage
- ⚠️ For production, update CORS policy and use HTTPS

---

## 🚢 Production Deployment

### Before Going Live:

1. **Update API URL** in `config.js`
   ```javascript
   api: {
       baseUrl: 'https://api.yourdomain.com'
   }
   ```

2. **Enable HTTPS** on both frontend and backend

3. **Update CORS** in backend:
   ```python
   allow_origins=["https://yourdomain.com"]
   ```

4. **Set up monitoring** and error logging

5. **Test thoroughly** with production data

---

## 📞 Troubleshooting Checklist

- [ ] Backend running on `localhost:8000`?
- [ ] Frontend accessible in browser?
- [ ] Network request shows 200 OK?
- [ ] Response contains `risk_probability`?
- [ ] Charts library (Chart.js) loaded?
- [ ] No CORS errors in console?
- [ ] Browser allows local file execution?

---

## 📚 Documentation

- **FRONTEND_SETUP.md** - Complete technical reference
- **INTEGRATION_GUIDE.md** - Architecture & design decisions
- **app/main.py** - Backend API documentation
- **app/schemas.py** - Data structure definitions

---

## 🎓 Learning Resources

### Frontend Code Organization
- `i18n.js` - Language management example
- `api-service.js` - API integration pattern
- `dashboard.js` - Component lifecycle
- `config.js` - Configuration management

### Backend (Study these for understanding)
- `app/main.py` - FastAPI endpoints
- `app/risk_logic.py` - Clinical algorithms
- `app/shap_explainer.py` - Model interpretation

---

## ✅ Verification

Run verification script:
```bash
python verify-setup.py
```

Should show:
```
✅ ALL CHECKS PASSED - Frontend is ready!
```

---

## 🎯 Next Steps

1. ✅ **Immediate**: Test the system as described above
2. ✅ **Review**: Read FRONTEND_SETUP.md for detailed documentation
3. ✅ **Customize**: Modify translations or add features as needed
4. ✅ **Deploy**: Follow production deployment guide
5. ✅ **Monitor**: Set up error tracking and analytics

---

## 💡 Pro Tips

- **Debug mode**: Open browser console (F12) to see detailed logs
- **API testing**: Use browser DevTools Network tab to inspect requests
- **Responsive test**: Press F12 → Toggle device toolbar (Ctrl+Shift+M)
- **Performance**: Check Network tab for load times

---

## 🎉 You're Ready!

Your CVD Risk Analytics system is fully functional and ready to use!

**Start the backend, open the frontend, and begin assessing cardiovascular risk.**

---

**Need help?** Check documentation files or review backend logs for error details.

**Version**: 1.0.0  
**Status**: Production Ready ✅
