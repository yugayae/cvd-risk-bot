# 📊 Google Sheets Data Logging Setup

This guide explains how to set up anonymous data logging to Google Sheets for research purposes.

---

## 🎯 Overview

The bot can log **anonymous** assessment data to Google Sheets with user consent:
- ✅ No Telegram ID or personal identifiers
- ✅ Only medical/health data
- ✅ Voluntary participation
- ✅ Used for research and model improvement

---

## 📋 Setup Steps

### 1. Create Google Sheets Spreadsheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create new spreadsheet
3. Name it: `CVD Risk Bot Data`
4. Add headers in row 1:
   ```
   A: timestamp
   B: consented
   C: region
   D: age
   E: gender
   F: ap_hi
   G: ap_lo
   H: cholesterol
   I: glucose
   J: height
   K: weight
   L: bmi
   M: smoke
   N: alcohol
   O: active
   P: risk_probability
   Q: risk_category
   R: shap_top_factor
   ```

### 2. Create Google Apps Script

1. In your spreadsheet: **Extensions → Apps Script**
2. Delete default code
3. Paste this code:

```javascript
function doPost(e) {
  try {
    // Get active spreadsheet
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    
    // Parse incoming data
    var data = JSON.parse(e.postData.contents);
    
    // Create row array
    var row = [
      new Date(),                           // timestamp
      data.consented || false,              // consented
      data.region || '',                    // region
      data.age || '',                       // age
      data.gender || '',                    // gender
      data.ap_hi || '',                     // systolic BP
      data.ap_lo || '',                     // diastolic BP
      data.cholesterol || '',               // cholesterol
      data.glucose || '',                   // glucose
      data.height || '',                    // height (cm)
      data.weight || '',                    // weight (kg)
      data.bmi || '',                       // BMI (calculated)
      data.smoke || '',                     // smoking
      data.alcohol || '',                   // alcohol
      data.active || '',                    // physical activity
      data.risk_probability || '',          // risk %
      data.risk_category || '',             // low/moderate/high
      data.shap_top_factor || ''            // top SHAP factor
    ];
    
    // Append row
    sheet.appendRow(row);
    
    // Return success
    return ContentService.createTextOutput(JSON.stringify({
      'status': 'success',
      'message': 'Data logged successfully'
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    // Return error
    return ContentService.createTextOutput(JSON.stringify({
      'status': 'error',
      'message': error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}
```

4. **Save** the script (💾 icon or Ctrl+S)
5. Name it: `CVD Bot Logger`

### 3. Deploy as Web App

1. Click **Deploy → New deployment**
2. Settings:
   - Type: **Web app**
   - Description: `CVD Bot Data Logger v1`
   - Execute as: **Me** (your Google account)
   - Who has access: **Anyone**
3. Click **Deploy**
4. **Authorize** the script (grant permissions)
5. **Copy the Web App URL**
   - Format: `https://script.google.com/macros/s/ABC.../exec`

### 4. Add URL to Bot Configuration

**Option A: Environment Variable (Render.com)**
1. Go to Render Dashboard
2. Your web service → Environment
3. Add variable:
   - Key: `GOOGLE_SHEETS_URL`
   - Value: `https://script.google.com/macros/s/ABC.../exec`
4. Save

**Option B: Local .env File**
1. Open `.env` file
2. Add line:
   ```
   GOOGLE_SHEETS_URL=https://script.google.com/macros/s/ABC.../exec
   ```
3. Save

### 5. Test the Integration

1. Restart bot (if local) or redeploy (if Render)
2. In Telegram, start new assessment
3. **Consent to data collection** when asked
4. Complete assessment
5. Check Google Sheet - new row should appear!

---

## 🔍 Troubleshooting

### No data appearing in sheet

**Check:**
- ✅ Web app deployed with "Anyone" access
- ✅ Script authorized (permissions granted)
- ✅ URL correct in environment variable
- ✅ User consented to data collection
- ✅ Bot logs show successful POST request

**Bot logs:**
```
# Success
INFO - Google Sheets logging successful

# Failure
WARNING - Google Sheets logging failed: [error]
```

### "Permission denied" error

**Solution:**
- Redeploy script with **"Anyone"** access
- Make sure "Execute as: Me" is selected

### Data format issues

**Check spreadsheet headers** match expected columns (see Step 1)

---

## 📊 Data Analysis

### Basic Queries

**Average risk by region:**
```
=AVERAGEIF(C:C, "East Asia", P:P)
```

**Count by gender:**
```
=COUNTIF(E:E, "male")
```

**Risk distribution:**
```
=COUNTIF(Q:Q, "high")
=COUNTIF(Q:Q, "moderate")
=COUNTIF(Q:Q, "low")
```

### Pivot Tables

1. Select all data
2. **Data → Pivot table**
3. Analyze by:
   - Region vs Average Risk
   - Age groups vs Risk category
   - Gender vs Risk probability

---

## 🔒 Privacy Compliance

### GDPR Compliance

✅ **Lawful basis:** Research with informed consent  
✅ **Data minimization:** Only health data collected  
✅ **Anonymization:** No personal identifiers  
✅ **Right to withdraw:** Users can decline anytime  
✅ **Transparency:** Clear explanation before collection  

### Best Practices

- ✅ Regular data backups
- ✅ Restricted sheet access (only authorized researchers)
- ✅ Periodic data review and cleanup
- ✅ Document data usage in research
- ✅ Never link to personal identifiers

---

## 🎓 Research Use Cases

### Model Improvement

- Identify underrepresented demographics
- Detect data drift over time
- Validate model performance in real-world

### Clinical Insights

- Regional risk patterns
- Lifestyle factor correlations
- Risk distribution analysis

### Quality Assurance

- Monitor prediction consistency
- Detect edge cases
- Validate SHAP explanations

---

## 📝 Sample Data Format

Example logged row:

```
timestamp:        2025-02-09 14:30:00
consented:        TRUE
region:           East Asia
age:              45
gender:           male
ap_hi:            140
ap_lo:            90
cholesterol:      2
glucose:          1
height:           175
weight:           80
bmi:              26.1
smoke:            1
alcohol:          0
active:           1
risk_probability: 0.234
risk_category:    moderate
shap_top_factor:  Systolic BP: 140 mmHg
```

---

## ⚠️ Important Notes

1. **Never store Telegram IDs** - violates privacy
2. **Review logged data periodically** - ensure anonymity
3. **Use for research only** - not for commercial purposes
4. **Keep access restricted** - share sheet only with researchers
5. **Document consent** - maintain transparency

---

## 🆘 Support

Issues with Google Sheets integration?
- Check bot logs for error messages
- Verify Apps Script permissions
- Test with manual POST request
- Create GitHub issue if persistent

---

**Data logging is optional but valuable for improving the model!** 📊✨
