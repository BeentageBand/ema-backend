from email.message import EmailMessage


class EventConfirmationEmail:
    def __init__(self, from_email, to_email, event):
        self.message = EmailMessage()
        self.message['Subject'] = f'Confirmation Email for {event.name}'
        self.message['From'] = from_email
        self.message['To'] = to_email

        content = f'''
        Congratulations!
        You have been invited to :
        Event : {event.name}
        Date : {event.begin_date}
        At : {event.location}
        This is RVSP.
        '''
        self.message.set_content(content)

    def get_message(self):
        return self.message
