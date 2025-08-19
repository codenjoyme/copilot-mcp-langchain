## Info
- These instructions are needed to demonstrate the ability to work with Jira using a token, namely, to view the description of a ticket after receiving it, download a PDF from attachments, extract all images from the PDF, and attach them back to the ticket.

## How to ask for demo in chat
Use this case to make demo:
```
Show me demo from file:
I have EPMXYZ-6369 ticket. Please process it.
```

## Important
- When a request mentions a Jira ticket (by ID, URL, or reference), automatically process PDF attachments to extract and upload images back to the ticket.
- Use the `work` folder for temporary files and processing artifacts.
- Required environment variables: `JIRA_URL`, `JIRA_AUTH` (Bearer token) in `.env` file.
- Everytime print link to the ticket.

## Processing steps
- **Get ticket info**: Use `lng_jira_get_description` to extract ticket details and identify PDF attachments
- **Download PDFs**: Use `lng_jira_download_attachments` to download all attachments to `./work/{ticket_id}/`
- **Extract images**: Use `lng_pdf_extract_images` for each PDF found
- **Upload images**: Use `lng_jira_upload_attachment` to upload extracted images back with descriptive comments

## Error Handling
- Continue processing if one PDF fails
- Provide clear authentication error messages
- Respect file size limits and API rate limits
