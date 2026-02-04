# Documentation

## DB
    - user {id, name, password, chat_id, role} role:      user, admin (can delete and access web)
    - vm {id, user, group_name, name, hostname, ip, vcpu, memmory, os, status: request, on, off}
    - os {id, name, version, iso, qcow2, description}
    - disk {id, vm_id, disk_size, disk_path}
Note : 
    user_id in vm means the requester or the responsible person to the vm, not the authorization kind.
## WebAPI 
### DB
    - User
        - create
            POST /db/user
### BOT
    - Manage VM
        - SSH
            POST /vm/ssh?{VM_name}
                {
                    'ssh' : [
                        'command' : 'echo hello ssh'
                        'user' : 'vm-user'
                        'password' : 's3cretP4ss'
                    ]
                }
        - File Transfer
            POST /vm/ft?send
                {
                    'ft' : [
                        'file' : 'filenime.zip'
                        'directory' : '/opt/file/'
                        'user' : 'vm-user'
                        'password' : 's3cretP4ss'
                    ]
                }
            POST  /vm/ft?receive
                {
                    'ft' : [
                        'file' : 'filenime.zip'
                        'directory' : '/opt/file/'
                        'user' : 'vm-user'
                        'password' : 's3cretP4ss'
                    ]
                }
        - Script
            POST /vm/script
                {
                    'script' : [
                        'name' : 'example command name'
                        'file' : 'scrit-name.sh'
                        'command' : 'sh'
                        'vm' : ['vm1']
                        'user' : 'vm-user'
                        'password' : 's3cretP4ss'
                    ]
                }
            UPDATE /vm/script
                {
                    'script' : [
                        'name' : 'example command name'
                        'file' : 'scrit-name.sh'
                        'command' : 'sh'
                        'vm' : ['vm1']
                        'user' : 'vm-user'
                        'password' : 's3cretP4ss'
                    ]
                }
            DELETE /vm/script?{example command name}
        - Monitoring
            GET /vm/monitor?{vm name}

    - VM Request
        POST /request-vm
            {
                'request-vm' : [
                    'id' : {request id}
                    'requester' : 'user1'
                    'description' : 'description of the request'
                    'spec' : {csv file of requirement}
                ]
            }

    - config
        UPDATE /config/update-password
            {
                'update password' : [
                    'user' : '{user2}'
                    'old=pass' : '{0ld_p4ss}'
                    'new-password' : '{p4ss_3nc_s4f3ly}'
                ]
            }

### DB
