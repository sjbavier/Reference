# Working with Electronic Mail

Email terms

- Mail User Agent (MUA)
  - program that sends mail from a computer to an MTA (SMTP)
- Mail Transfer Agent (MTA)
  - delivers email from sending server to delivery server (SMTP)
  - or between other MTAs (SMTP)
- Mail Submission Agent (MSA)
  - accepts mail from the MTA (may be all inclusive or separate program)
- Mail Delivery Agent (MDA)
  - delivers messages to mail spool (may be all inclusive or separate program)

Post Office Protocol

- Downloads mail from the MTA
- POP
  - POP3 - port 110
  - POP3s - port 995 uses SSL
  - defaults to deleting mail from MTA upon downloading
- IMAP - Internet Mail Access Protocol
  - more powerful, downloads a copy only
- Smart Host or Mail Relay
  -

Email structure

- Sender's ID
- Sender's domain
- Destination email address
- Subject line
- Message data

## Simple Mail Transfer Protocol (SMTP)

- runs on IP
- uses TCP and UDP port 25

