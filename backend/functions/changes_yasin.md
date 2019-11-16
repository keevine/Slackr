1. Used helper function: get_u_id() to check whether email is already registered in auth_register. Code is further abstracted and more clear.

2. Added more comments to improve clarity of functions.

3. Abstracted joining process of user to eliminate redudancy of joining in
channel_invite and channel_join

4. Added helper functions to channel_details to remove redundant code that 
was previously in channel_create. channel_details now grabs all necessary 
information from just u_id through helper funcs.

5. Extracted code for checking name into a helper function as the same code,
for checking constraints on name was used in other functions. Removed redudancy 
and improved clarity

6. Removed unncessary statements like "== True", and replaced "!=" with Not. 
Improves readability

7. When appropriate, attached name-tags to "magic numbers" such that is clear,
what the numbers are used for. This was not necessary for very trivial cases, 
where it is immediately clear to the reader the purpose of the number.

8. Generate further helper functions to carry out mini-processes which 
accomplished 1 goal. E.g. seting permissions, generating handles. This decreased,
the size of auth_register and inturn made the function clearer.