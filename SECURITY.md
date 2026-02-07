# Security Policy

## 🔒 Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## 🚨 Reporting a Vulnerability

### For Security Issues

**DO NOT** create a public GitHub issue.

Instead:
1. Email: Create a private issue with label `security`
2. Include:
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Time

- Initial response: Within 48 hours
- Fix timeline: Depends on severity
  - Critical: 24-48 hours
  - High: 1 week
  - Medium: 2 weeks
  - Low: Next release

## 🛡️ Security Measures

### Current Protections

- ✅ Input validation (Pydantic)
- ✅ Rate limiting (10/day per user)
- ✅ No data storage
- ✅ Timeout protection
- ✅ CORS configuration
- ✅ Environment variable protection

### Best Practices

1. **Never** commit tokens or secrets
2. **Always** use environment variables
3. **Review** dependencies regularly
4. **Update** packages for security patches
5. **Monitor** logs for suspicious activity

## 🔐 For Developers

### Secure Coding

```python
# ❌ Bad - hardcoded token
BOT_TOKEN = "123456:ABC..."

# ✅ Good - environment variable
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
```

### Dependencies

- Run `pip audit` regularly
- Update dependencies for security patches
- Pin versions in requirements.txt

### API Keys

- Store in `.env` (never commit!)
- Rotate keys regularly
- Use different keys for dev/prod

## ⚠️ Medical Data

This bot does NOT store patient data:
- No database
- No logs of medical info
- No user tracking (except usage counts)

## 📞 Contact

For security concerns:
- Create a private issue
- Email project maintainers

Thank you for keeping the project secure! 🙏
