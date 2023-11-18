1. tutorials - lessons given by a teacher, every lesson should accomplish sth - this has to be centered around particular, specific things to do. Don't explain alternatives, options, notions
   1. link to installation (on github)
   2. authorization
   3. craete and delete bucket, list bucket
   3. simple upload
   4. simple download
   5. directory upload
   6. directory download
   7. deleting files
   8. hiding files
   9. deleting specific file version (maybe finding by file name)
   10. key creation
2. how to guides - recipes that are goal oriented. These guides can assume basic competence. No explanations here. Some
   flexibility is welcome, so it's easy to adapt the guide to a slightly different scenario. Practical usability is more
   important than completeness - so we don't have to cover every single detail
   1. bucket for static files - public
   2. bucket for backups - with a write only key and an exemplary psql piped to b2 upload
   3. replication
   4. temporary keys?
   5. sync
   6. rclone
   7. s3 compatible - how to use s3-capapble tools with b2 instead of s3
   8. lifecycle rules
   9. bash completion
   10. signed links
3. reference guides - information oriented, list of all commands and other notions improtant to the domain. The structure of the  reference guide should mirror the structure of the domain. All about profiles needs to go here. AND SQLITE and env vars. and encyption. and sync. and legal hold. B2_USER_AGENT_APPEND. REALM, DEVELOPMENT URL. Logging. all env vars used.
   
4. explanations - oriented towards understanding.
   1. versions, hiding etc
   2. sync?