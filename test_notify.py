from notifier import send_summary, make_voice_call

msg = "📧 From: noreply@vitstudent.ac.in\nSubject: Test\n\nDr. V. Samuel Rajkumar has an update."
print('Calling send_summary...')
send_summary(msg)
print('Calling make_voice_call...')
make_voice_call(msg)
print('Done')
