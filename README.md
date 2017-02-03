## Morgenmadsliste

En hjemmeside bygget oven på en REST API der har til formål at hjælpe KSM med at styre hvem der skal 
have morgenmad med hver fredag.

### Features
- Bruger system
    - Log in
    - Log ud
    - Profil side
        - Muligt at ændre brugerinfor
    - Email reminder
        - Reminder til den der skal have med
        - Reminder til alle om at bekræfte at de kommer til morgenmad
    - SMS reminder?
    
### API
/api/user

GET: Liste over alle brugere

GET /<id>: En specific bruger