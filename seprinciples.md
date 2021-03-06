## Changes to `auth_functions`

1. Used helper function: `get_u_id` to check whether email is already registered in `auth_register`. Code is further abstracted and more clear.

2. Added more comments to improve clarity of functions.

3. Generate further helper functions to carry out mini-processes which
accomplished 1 goal. E.g. setting permissions, generating handles. This decreased
the size of `auth_register` and in turn made the function clearer.

4. Extracted code for checking name into a helper function as the same code,
for checking constraints on name was used in other functions. Removed redundancy
and improved clarity

5. Removed unnecessary statements like "== True", and replaced "!=" with Not.
Improves readability

6. When appropriate, attached name-tags to "magic numbers" such that is clear,
what the numbers are used for. This was not necessary for very trivial cases,
where it is immediately clear to the reader the purpose of the number.


## Changes to `channel_functions`

1. Helper function was created: `remove_from_list`.
This was done since the same loop was done for multiple functions: `channel_leave` & `channel_removeowner`.
The process of removing a user from a specific list in the database was abstracted and made simpler for
the mentioned functions.

2. Helper functions replaced starting code wherever possible for error handling. E.g. When checking
if the channel ID is valid, `is_valid_channel` would be called. This would keep the code simpler
and easier to read.

3. Pylint was used extensively within this file and the pytests in order to get a better gauge of style and presentability.
e.g. the wildcard imports were all removed in favour for direct import statements.

4. Abstracted joining process of user to eliminate redundancy of joining in
`channel_invite` and `channel_join`. This made the function easier to follow
whilst also removing unncessary code.

5. Added helper functions to `channel_details` to remove redundant code that
was previously in `channel_create`. `channel_details` now grabs all necessary
information from just u_id through helper funcs.

## Changes to `message_functions`

1. Created get_channel_id helper function for obtaining a channel_id from a message_id. This is used in message_pin/unpin

2. Created remove_channel_message_dict helper function for removing channel specific message dicts. This is used in message_remove

3. Abstracted some code by using helper functions to help remove clutter in main functions

4. Created more tests for conditions not met in coverage e.g. some access errors in react/unreact test

5. Fixed up reacts from iteration 2 to constantly update and check in channel messages

6. Cleaned up imports to only include necessary imports 

7. Fixed issues with indenting and casing along with various general formatting

8. Removed unnecessary statements e.g. "==" and "!=" replaced with 'not'

9. Removed magic numbers by using nametags to help improve readability for users

## Changes to `profile_functions` & `misc_functions`

1.  Commenting was added in order to apply the K.I.S.S concept. Comments were used to describe the purpose and function of each
module of logic, and as such, were placed as a header for readability, for each module.

2. Reapplying helper functions. Helper functions were utilised as part of the D.R.Y requirement, to shorten and simplify code. Examples include
retrieving a key from a data dictionary. The provided handle function reduced unnessesary repetition at the start of each function, as well as
providing a meaningful abstraction handle, e.g "user_dict" in order to provide a clear and meaningful abstraction.

3. Incremental Development is a pivotal software engineering and was utilised through the application of continous testing. During the writing of
functions, important return statements and the raising of errors was implemented first. Once this was completed, the function underwent testing to ensure
the correct result was always returned. From the certified success and satisfactory result of testing, further development followed. This cycle was repeated
for the implementation of all the functions.

4. Consistency is important in the restructuring of the code, frequent communication between members demanded a standardised layout and quality of work. As such,
once a unanimous decision was reached on the basis of our code style, all members re-evaluated their code to this new standard. Notable changes include the calling of
helper functions, standardised variable names, indentation and whitespace.

5.  Anticipation of change. As we were pre-emptively informed of changing specifications, we wrote the code to accomodate to future reprises. This was based off the vague definition of the specification provided, thus accomodating space for improvements. Standups are a case study, once implemented, as a team during implementation 2, we came to the conclusion that there was no certified method to determine if a standup was still running or not. As such, as a team, we made sure when a redefinition was released, we could easily intergrate the solution, through the presence of code comments on the best possible insertion point for the solution. This contingency plan was used when the addition of standup/active was announced, and there were little to no issues in modifying the code with consideration to the new changes

6. Removal of unecessary code. In order to comply with Y.A.G.N.I, re-evaluation provide valuable in the removal of unecessary code, particularly, the presence of helper functions and scaffolding code, made redundant by changing specifications. A perfect example is the alteration and removal of several standup fields inside the channel dictionary, that was present in iteration 2, due to the undefined nature of the standups at the time. As a result of a new, clear definition, obselete code and helper functions pertaining to the outdated standup model, were removed
