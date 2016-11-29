# KaaS Askarl v1.0.2
Askarl, a simple RESTful interface to a KaaS (Karlettin as a Service) implementation.

## Usage
A working version is available at http://ask.dataninja.it/. First you have to register a personal account,
obtain a token for your later requests and add money to your budget: http://ask.dataninja.it/for/token?name=Your+Name&budget=2k.

Finally you can ask Karl (don't forget the offer!):
http://ask.dataninja.it/to/karl?token=your-token&budget=5&question=Dove+trovo+i+dati+sulle+frodi+informatiche.

Be careful, every answered question decreases your budget of your offer. When all your money has gone, you can refill the budget
(http://ask.dataninja.it/for/token?token=your-token&budget=100) and keep asking to karl.

If something goes wrong, please read the error description carefully. And if you think there is a bug,
please [open a new issue](https://github.com/Dataninja/kaas-askarl/issues/new).

And remember: don't ask to ask karl, just ask!

### /for
Prefix to manage your personal account.

#### /for/token
Register a new user providing your name.
Managed parameters are listed if no one is provided.

* n or name (required): user name
* b or budget (required): money to add to budget (in euros, ie. 5 or 2k)
* r or reply-to: how do you want to get the answer if not provided when asking?
 * now (wait for the reply, default)
 * a valid email address
 * a valid callback url (webhook)

Success response register the user and return the personal token.
Annotate it for later queries!

Examples:

* http://ask.dataninja.it/for/token?name=Your+Name (no budget)
* http://ask.dataninja.it/for/token?name=Your+Name&budget=2k (start with 2,000 €)

WARNING: data are not crypted, nor safely stored and can be public available, so don't send sensitive data in your name.

#### /for/user
Show informations about registered user from token and add money to personal budget.
Managed parameters are listed if no one is provided.

* t or token (required): a valid token of a registered user
* b or budget (required): money to add to budget (in euros, ie. 5 or 2k)

Examples:

* http://ask.dataninja.it/for/user?token=your-token (show info)
* http://ask.dataninja.it/for/token?token=your-token&budget=100 (add 100 € to your budget)

#### /for/remove
Remove a registered user.
Managed parameters are listed if no one is provided.

* t or token (required): a valid token of a registered user

### /to
Prefix to query available bots of the installed KaaS instance.

#### /to/[bot]
Query to [bot]. Available bots are listed at */to*.
Managed parameters are listed if no one is provided.

* t or token (required): a valid token of a registered user
* q or question (required): the question, an URL encoded text (ie. "Dove trovo dati sul tasso di natalità?")
* b or budget (required): how much money are you willing to offer (in euros, ie. 5 or 2k)?
* m or mode: you hurry?
 * fast (default)
 * accurate
 * fa (fast AND accurate)
* r or reply-to: how do you want to get the answer?
 * now (wait for the reply, default)
 * a valid email address (not implemented)
 * a valid callback url (webhook, not implemented)

Examples:

* http://ask.dataninja.it/to/karl?token=your-token&budget=5&question=Dove+trovo+i+dati+sulle+frodi+informatiche (5 € waiting for a fast response)
* ...

## Installation
Clone the repository, change the service port if needed and run the service: `python askarl.py`.
Open http://localhost:54234 (or using your customized port) and use the service.
Registered accounts are stored in a *tokens.db* file in pickle format and listed at */for/tokens*.

## Credits
Made with love by [Alessio "jenkin" Cimarelli](https://github.com/jenkin) for [Dataninja](https://github.com/Dataninja/) & friends.

