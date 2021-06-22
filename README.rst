*****************
Simple DYN365
*****************
Simple DYN365 is a simple Microsoft Dynamics365 Web API client, it provides full CRUD functionality and eases use of Micorost Dynamics Web API, responses are returned in form of dictionary JSON.

=============

More about Web API can be found at:
https://docs.microsoft.com/en-us/powerapps/developer/data-platform/webapi/overview

Examples
--------------------------
There are two ways to gain access to Dynamics

The first is using client credentials which is to simply pass the CRM Org link, client ID, client Secret, TenantID

For example:

.. code-block:: python

    from simple_dyn365 import Dynamics
    dyn = Dynamics(client_id='47xxxx37-xxxx-4837-bxx6-5fxxxx2a07e', client_secret='nb4gh5jtbKG.MWASDTU-bLqP~9YCFt-n', tenant_id='cxxxx58c-xxxx-4d8a-ac2e-1a8dxxxxfbb4', crm_org='https://myenvname.crm.dynamics.com')

The second way is using password, but this is still not implemented yet.

Record Management
--------------------------

To create a new 'Contact' in Dynamics:

.. code-block:: python

    dyn.contacts.create({'firstname' : 'Adam', 'email' : 'adam@adam-ma.dev'})

This will return a string of response such as ``'https://myenvname.crm.dynamics.com/api/data/v9.2.21051.00140/contacts(96c5a6d3-28d3-eb11-bacc-000d3a57991e)'``

To get a dictionary with all the information regarding that record, use:

.. code-block:: python

    contact = dyn.contacts.get('96c5a6d3-28d3-eb11-bacc-000d3a57991e')


To change that contact's first name from 'Adam' to 'John' and add a last name of 'Mahameed' use:

.. code-block:: python

    dyn.contacts.update('96c5a6d3-28d3-eb11-bacc-000d3a57991e',{'firstname': 'John', 'lastname': 'Mahameed'})

To delete the contact:

.. code-block:: python

    dyn.contacts.delete('96c5a6d3-28d3-eb11-bacc-000d3a57991e')


Note that Update, Delete and Upsert actions return the associated `HTTP status codes <https://docs.microsoft.com/en-us/powerapps/developer/data-platform/webapi/compose-http-requests-handle-errors>`_


Use the same format to create any record, including 'accounts', 'contacts', and 'annotations'.
Make sure to have all the required fields for any entry. The `Web API`_ has all entities and their fields.

.. _Web API: https://docs.microsoft.com/en-us/dynamics365/customer-engagement/web-api/entitytypes?view=dynamics-ce-odata-9

Queries
--------------------------

It's also possible to write select queries in Dynamics

Queries are done via:

.. code-block:: python

    dyn.query("contacts?$select=fullname,contactid")

It can also be done in the following way:

.. code-block:: python

    dyn.contacts.query("select=fullname,contactid")


Other Options
--------------------------


To retrieve basic metadata use:

.. code-block:: python

    dyn.contacts.metadata()

To upload Base64 object, use:

.. code-block:: python

    dyn.annotations.upload_base64(file_path='myimage.png', base64_field='documentbody' data={'subject' : 'Some subject', 'notetext' : 'Some text for the sweet note', 'objectid_contact@odata.bind' : 'contacts(02125b8c-9ed2-eb11-bacc-000d3a57991e)', 'filename' : 'myimage.png'})

To update Base64 object, use:

.. code-block:: python

    dyn.annotations.update_base64(entity_id='65bb00b9-99d2-eb11-bacc-000d3a57991e',base64_field='documentbody', file_path='newimg.png'))

To retrieve a Base64 object:

.. code-block:: python

    base64_data = dyn.annotations.get_base64('65bb00b9-99d2-eb11-bacc-000d3a57991e', base64_field='documentbody')
    with open('img.png', 'wb') as f:
         f.write(base64_data)

      

Author & License
--------------------------
This package is released under MIT license. Simple-DYN365 was written by `Adam Mahameed`_, its idea was taken from implementation of simple-salesforce REST API package.

`GitHub`_

.. _Adam Mahameed: https://github.com/adam-mah
.. _GitHub: https://github.com/adam-mah/simple-dyn365