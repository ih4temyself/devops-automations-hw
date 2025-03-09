#!/bin/bash
user=${DEFAULT_USER}
home_dir=/home/$user
mkdir -p $home_dir/.ssh
chmod 700 $home_dir/.ssh
echo '${YOUR_PUBLIC_KEY}' >> $home_dir/.ssh/authorized_keys
echo '${MY_PUBLIC_KEY}' >> $home_dir/.ssh/authorized_keys
chmod 600 $home_dir/.ssh/authorized_keys
chown -R $user:$user $home_dir/.ssh