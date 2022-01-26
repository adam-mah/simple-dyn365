| To be able to use simple-dyn365 with Dynamics environment, please follow the following steps to allow API access:   
| 
| App registration:   
1. Login to azure.microsoft.com with Dynamics users.
2. Open Azure portal. 
3. Go to Manage Azure Active Directory. 
4. Click App registrations
5. New registration
6. Set any name u want and click register
7. Open newly registered app, click o client credentials and generate a new client secret
8. Save the key “Value”
9. Save “Application (client) ID” and “Directory (tenant) ID”

| Authorizing app user:
1. Open Dynamics CRM
2. Click settings -> Advanced settings
3. Click “Settings” dropdown arrow and select “Security”
4. Click “Users”
5. Select “Application Users” from dropdown (Where Omnichannel is selected)
6. Click “NEW”
7. Insert the registered app Application ID in “Application ID” field
8. Click Save
