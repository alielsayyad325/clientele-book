# 🔧 Dev TODO – ClienteleBook Enhancements

## 🔐 Forgot Password – Full Flow Implementation

**Status:** Placeholder UI live – reset functionality still pending

---

### ✅ Phase 1: Token + Email (Pending)
- [ ] Use `itsdangerous.URLSafeTimedSerializer` to generate a time-limited token
- [ ] Link token to a secure route: `/reset-password/<token>`
- [ ] Store email lookup and verification in the flow
- [ ] Protect token from reuse or expiration exploits

---

### ✅ Phase 2: Email Delivery
- [ ] Use `Flask-Mail` to send password reset email
- [ ] Use branded HTML email template (match app tone)
- [ ] Include call-to-action: “Reset Your Password”
- [ ] Confirm delivery success/failure logging

---

### ✅ Phase 3: Password Reset Page
- [ ] Render `/reset-password/<token>` route if token is valid
- [ ] Create secure password update form
- [ ] Update password in DB after validation
- [ ] Auto-expire token or invalidate on password change

---

### 💡 Considerations:
- Add audit trail/logging for admin resets
- Consider CAPTCHA/Rate limiting on forgot password
- Add notification to account email on password change

---

📅 Target Implementation: TBD
