from notifier import send_summary

msg = "📧 From: noreply@vitstudent.ac.in\nSubject: Test\n\nDr. V. Samuel Rajkumar has an update."
print('Calling send_summary...')
send_summary(msg)
print('Done')
