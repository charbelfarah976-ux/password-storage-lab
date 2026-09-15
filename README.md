# Password Storage Lab

An interactive CSC316 teaching project that stores one fictional registration
in three deliberately different ways:

1. Plaintext
2. SHA-256 without a salt
3. SHA-256 with a unique, deterministic per-user salt

The web interface makes the security difference visible, implements the
optional login-verification bonus, and automatically detects the strongest
experiment: two different users choosing the same demonstration password.

> **Educational warning:** This repository intentionally demonstrates insecure
> password storage. Never enter a real password, publish the generated database,
> or reuse this three-table design in a production system.

## Features

- Polished responsive Flask web interface
- Three real SQLite tables matching the assignment
- One UUID and timestamp shared across all three records for each registration
- SHA-256 provided by Python's standard `hashlib` library
- Reproducible salt derived from username, user ID, and registration timestamp
- Atomic database writes, preventing partially stored registrations
- Side-by-side display of all three storage outcomes
- Complete view of all three database tables
- Correct-password, wrong-password, and unknown-user verification states
- Timing-resistant comparison through the standard `hmac` library
- Same-password reuse insight across multiple users
- Automated tests covering the security properties and web flows
- Render-ready production server and deployment blueprint
- Public-demo privacy headers, no-cache policy, and search-indexing opt-out
- No external front-end framework or online asset dependency

## Quick start

Python 3.10 or newer is recommended.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 app.py
```

Open <http://127.0.0.1:5050> in a browser.

Port `5050` is used locally because macOS Control Center/AirPlay Receiver can
occupy port `5000`.

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Public link for an instructor

`127.0.0.1` always means "this computer," so it cannot be shared with an
instructor. A public GitHub repository also displays the source code but does
not run the Python application. The included `render.yaml` deploys the app as a
free Render web service using Gunicorn.

See [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) for the exact public deployment
steps and important SQLite/privacy behavior.

The hosted classroom version uses temporary storage deliberately. On Render's
free service, the SQLite database is erased whenever the service restarts or
spins down. This keeps fictional classroom submissions from persisting, but it
also means the instructor may need to recreate the two sample users after a
cold start.

## Best demonstration sequence

Use invented credentials only.

1. Register `demo_alice` with `UniDemo!123`.
2. Examine the three storage result cards.
3. Register `demo_bob` with the same `UniDemo!123` password.
4. Observe that Table 2 contains the same unsalted hash for both accounts.
5. Observe that Table 3 contains different salts and different salted hashes.
6. Verify `demo_alice` with the correct password.
7. Verify the account again using an incorrect password.
8. Try an unknown username and the registration validation cases.

The application automatically displays a same-password insight after step 3.

## Required data structures

The SQLite schema contains exactly the three assignment tables, with one useful
`registered_at` extension:

```text
password_plain
  user_id | username | password_plain | registered_at

password_hash
  user_id | username | password_hash | registered_at

password_salted
  user_id | username | salt | password_salted_hash | registered_at
```

The same `user_id`, `username`, and registration time are used in all three
rows. The three inserts occur in one transaction so they all succeed or all
fail together.

## Transformations

The application calls existing implementations in Python's standard library;
it does not implement a hashing algorithm.

### Table 1 — plaintext

```text
stored value = password
```

This is intentionally and critically insecure.

### Table 2 — unsalted SHA-256

```text
password_hash = SHA-256(password encoded as UTF-8)
```

Equal passwords create equal hashes, exposing password-reuse patterns and
allowing one common-password guess to be compared with many accounts.

### Table 3 — salted SHA-256

The known salt inputs are serialized as an unambiguous compact JSON array:

```text
salt_material = [username, user_id, registration_timestamp]
salt = SHA-256(salt_material encoded as UTF-8)
password_salted_hash = SHA-256(salt + password)
```

The UUID makes the salt unique per user. The stored registration timestamp and
identity values make the construction reproducible and explainable, as required
by the assignment.

## Login verification

The password attempt is checked without reversing either hash:

```text
Table 1: attempt == stored plaintext
Table 2: SHA-256(attempt) == stored password hash
Table 3: SHA-256(stored salt + attempt) == stored salted password hash
```

A correct password should match all three representations. A wrong password
should match none of them. This demonstrates that all three methods can verify
a password even though they offer very different protection after a database
breach.

## Running the automated checks

With the virtual environment active:

```bash
python3 -m pytest
```

The checks cover:

- The known SHA-256 output for a standard test value
- Deterministic hashing and salt derivation
- Salt uniqueness between users
- Different salted hashes for the same password
- One synchronized record in every table
- Atomic duplicate rejection
- Successful and failed login verification
- Missing input and unknown-user cases
- Unicode input support
- The same-password experiment

## Resetting the demonstration database

The app creates `instance/password_lab.sqlite3` automatically on first launch.
To erase all local demo registrations and recreate the tables, run:

```bash
flask --app app init-db
```

This reset is destructive to local demonstration data. The database is ignored
by Git because Table 1 intentionally contains plaintext values.

## Project structure

```text
.
├── app.py                         # Local development entry point
├── render.yaml                    # Free Render web-service blueprint
├── .python-version                # Deployment Python version
├── docs/
│   ├── DEPLOYMENT.md              # Public-link instructions and caveats
│   └── STUDY_AND_REPORT_GUIDE.md  # Oral defense, report, and screenshots
├── password_lab/
│   ├── __init__.py                # Application factory and routes
│   ├── db.py                      # Atomic SQLite operations and queries
│   ├── schema.sql                 # Three assignment tables
│   ├── security.py                # Standard-library hash transformations
│   ├── static/
│   │   ├── app.js                 # Password visibility and result scrolling
│   │   └── styles.css             # Responsive visual design
│   └── templates/
│       ├── base.html              # Shared page structure
│       └── index.html             # Complete interactive dashboard
└── tests/
    ├── conftest.py
    ├── test_app.py
    └── test_security.py
```

## Suggested report screenshot states

To satisfy the requirement to document every supported result, capture:

1. Initial empty database state
2. Missing username validation
3. Missing password validation
4. Successful registration and three comparison cards
5. Duplicate username rejection
6. Same-password experiment with two fictional users
7. Correct password verification
8. Incorrect password verification
9. Unknown username verification
10. Complete contents of all three database tables

Keep the names and passwords obviously fictional. Each report image needs a
one- or two-sentence explanation.

## Classroom design versus real-world security

This project follows the assignment's deterministic salt rule so the process is
easy to reproduce and explain. Real systems normally use a cryptographically
random salt generated by a password-hashing library.

Even with a unique salt, SHA-256 remains too fast for production password
storage. A real authentication system should use a deliberately slow,
memory-hard password-hashing function such as Argon2id, or an appropriate
alternative such as bcrypt, scrypt, or PBKDF2.
