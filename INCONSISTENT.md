Inconsistenticies to fix:

1. file-info with b2:/. does not contain `contentMd5` and with b2id:// does

2. if key does not have read access `isFileLockEnabled` property should be set to `unknown` (currently: `"isFileLockEnabled": null`)

3. what does `defaultRetention` `null` mean? does it mean that it is none?:

    "defaultRetention": {
        "mode": null
    },

check this


Even: introduce a possible value of "mode": "unknown" and for buckets with no default encryption use "mode": null.


4. delete-bucket, succesed silently

deleting file version with delete-file-version ouputs json

5. creating new bucket does not return json, just the bucket id

6. list buckets does not return json but something else

check other commands

create-key. delete-key, list-buckets