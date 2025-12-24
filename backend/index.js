import "dotenv/config";
import express from "express";
import cors from "cors";
import { Resend } from "resend";

const app = express();

const ALLOWED_ORIGIN = process.env.ALLOWED_ORIGIN || "*";
app.use(cors({ origin: ALLOWED_ORIGIN }));
app.use(express.json({ limit: "200kb" }));

if (!process.env.RESEND_API_KEY) {
  console.warn("Missing RESEND_API_KEY");
}
const resend = new Resend(process.env.RESEND_API_KEY);

app.get("/health", (_, res) => res.json({ ok: true }));

app.post("/api/contact", async (req, res) => {
  try {
    const { name, email, message } = req.body || {};

    if (!name || !email || !message) {
      return res.status(400).json({ ok: false, error: "Missing fields." });
    }
    if (String(message).length > 5000) {
      return res.status(400).json({ ok: false, error: "Message too long." });
    }

    const from = process.env.CONTACT_FROM;
    const to = process.env.CONTACT_TO;

    if (!from || !to) {
      return res.status(500).json({
        ok: false,
        error: "Server not configured (CONTACT_FROM / CONTACT_TO).",
      });
    }

    const subject = `New contact form message from ${name}`;

    const html = `
      <div style="background:#f4f6f8;padding:32px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
        <div style="max-width:640px;margin:0 auto;background:#ffffff;border-radius:12px;box-shadow:0 6px 20px rgba(0,0,0,0.08);overflow:hidden;">
      
          <!-- Header -->
          <div style="background:#111827;color:#ffffff;padding:20px 28px;">
            <h1 style="margin:0;font-size:20px;font-weight:600;">
              Worksheet AI
            </h1>
            <p style="margin:6px 0 0;font-size:13px;color:#c7d2fe;">
              New Contact Form Submission
            </p>
          </div>

          <!-- Body -->
          <div style="padding:28px;color:#111827;">
            <table style="width:100%;border-collapse:collapse;">
              <tr>
                <td style="padding:8px 0;font-weight:600;width:90px;">Name</td>
                <td style="padding:8px 0;">${escapeHtml(name)}</td>
              </tr>
              <tr>
                <td style="padding:8px 0;font-weight:600;">Email</td>
                <td style="padding:8px 0;">
                  <a href="mailto:${escapeHtml(email)}" style="color:#2563eb;text-decoration:none;">
                    ${escapeHtml(email)}
                  </a>
                </td>
              </tr>
            </table>

            <hr style="margin:20px 0;border:none;border-top:1px solid #e5e7eb;" />

            <p style="margin:0 0 8px;font-weight:600;">Message</p>
            <div style="background:#f9fafb;border:1px solid #e5e7eb;border-radius:8px;padding:16px;white-space:pre-line;line-height:1.5;">
              ${escapeHtml(message)}
            </div>
          </div>

          <!-- Footer -->
          <div style="background:#f9fafb;padding:16px 28px;font-size:12px;color:#6b7280;text-align:center;">
            This message was sent from the Worksheet AI contact form.
          </div>

        </div>
      </div>
    `;

    const { data, error } = await resend.emails.send({
      from,
      to: [to],
      replyTo: email,
      subject,
      html,
    });

    if (error) {
      return res.status(500).json({ ok: false, error: error.message });
    }

    return res.json({ ok: true, id: data?.id });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ ok: false, error: "Server error." });
  }
});

function escapeHtml(str) {
  return String(str)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

const PORT = process.env.PORT || 5050;
app.listen(PORT, () => console.log(`Contact API running on :${PORT}`));
