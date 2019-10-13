As a user, I want a search bar function, so that I can access archived messages faster and reduce the time taken to find related messages.
==============================================
User Acceptance Criteria
-The search field is placed on the top
-Search starts once the user clicks search
-The field contains a placeholder stating "Search a word"
-The aforementioned placeholder dissapears once the user starts typing
-Search is performed by the user as long as the field is not empty
Acceptance Tests
-Search field is clearly visible
-Search function will not run with the placeholder
-Search function will not run on empty strings
-The function will return "No results" if no results are found


As a user, I want a profile picture, so I can identify others effeciently on the platform 
==============================================
User Acceptance Criteria
-The profile picture is shown on the user profile
-The profile picture is a square, other sizes must be cropped
-The profile picture by default is a grey silhouette
-The profile picture can be changed by clicking on "Change profile picture"
-The profile picture must be between a minimum and maximum size
Acceptance Tests
-The user can find and upload a picture as their profile picture
-The user cannot upload a picture with invalid dimensions e.g too large too small
-The user can upload rectangular pictures, and will then crop to size
-The user can upload photos of the minimum and maximum size

As a user, I want social media links, so that others can contact me through alternative means at any time.
==============================================
User Acceptance Criteria
-Social media links are displayed on the user profile
-Common social media links are used, i.e facebook, twitter and linkedin
-Social media links are highlighted in the domains primary colours, e.g Facebook blue, Twitter Light blue
-Clicking the links will redirect to the users profile on other platforms
-If no links are entered, the links will not be shown
Acceptance Tests
-Facebook, LinkedIn, Twitter, Google+ links are recognised
-Invalid user profiles cannot be linked i.e Bad URL
As a user, I want to change my personal information, so that I can also push my latest contact details to others
==============================================
User Acceptance Criteria
-The user can change their details by clicking "Change details" button on their profile
-The fields contain the current information that can be changed to non-empty and valid information
-Only the user can change their own personal information
Acceptance Tests
-The user cannot leave required fields empty
-The user can change a non-required filled field to be empty

As a user, I want a username, so that I can keep my identity private unless divulged.
==============================================
User Acceptance Criteria
-The user is prompted to create a handle upon account registration.
-The user must not exceed 20 characters for their new handle
-Special characters are valid
-Empty handle is not valid
-The user can change their handle by clicking "Change details" button on their profile
-The user can only modify their own handle
Acceptance Tests
-The user can have a handle of pure special characters, up to and including 20 characters but not more
-Leading and trailing spaces are ignored
-The user cannot have an empty handle

As a admin, I want permission controls , so that I can set different users with different privileges and permissions 
==============================================
User Acceptance Criteria
-An admin or owner can promote or demote others
-The function is not avaliable for members
-The admin or owner will go to a users profile to change permissions
-A member cannot be demoted further nor a admin or owner promoted further
-The permission controls will feature a drop down box to select the new role of the specified user
-Only owners can promote other users to owner
Acceptance Tests
-The admin can promote a user to admin
-The owner can promote au user to admin and owner
-The member cannot access this control
-The admin and owner cannot demote a member
-The admin cannot demote a owner

As a user, I want dedicated support for standups, so that I can organise asynchronised standups that promote buisness
==============================================
User Acceptance Criteria
-Standups can be initiated by a "Start standup" button on the channel
-The standup will send a notification to users in the channel to remind them
-During the specified 15 minute window, sent messages will appear highlighted to show they are part of the standup
-At the end of the 15 minute window, highlighted messages will be summarised and avaliable to download on the channel settings
-Another standup cannot start until one is finished.
Acceptance Tests
-The resulting summary is downloadable
-If no messages are sent in the standup, no summary is generated
