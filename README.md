# Backend Template for User service

## Git Commit Style Guide
### Format of the Commit
```
{type}({scope}): {subject}
```
### Rules for Commit

#### Allowed Types - {types}
 - feat -> feature
 - fix -> bug fix
 - docs -> documentation
 - style -> formatting, lint stuff
 - refactor -> code restructure without changing exterrnal behavior
 - test -> adding missing tests
 - chore -> maintenance
 - init -> initial commit
 - rearrange -> files moved, added, deleted etc
 - update -> update code (versions, library compatibility)
#### Scope - {scope}
Where the change was (i.e. the file, the component, the package).
> It can be anything specifying place of the commit change e.g. the controller, the client, the logger, etc.
### Message Body - {body}
This gives details about the commit, including:

- motivation for the change (broken code, new feature, etc)
 - contrast with previous behavior
Some rules for the body:

Must be in present tense.
 - Should be imperative.
 - Lines must be less than 80 characters long.

### Example

```
fix(users): fix bug in user repository.
```
