#!/bin/bash

# Usernames
USERNAMES=(
  "furqan.nadeem"
  "khuram.arif"
  "m.usman"
  "ahsan.wali"
  "hasnat.ali"
  "fahad.mahmood"
  "idrees.faiq"
  "muhammad.shehryar"
  "arham.nawaz"
  "umair.khan"
  "hassan.tariq"
)

# Password (Same for all users)
PASSWORD="pJ`?5F{%67#0jG"  # Replace with the desired password

# Groups
DEVOPS_GROUP="devops"
MONITORING_GROUP="monitoring"

# Create groups
sudo groupadd $DEVOPS_GROUP
sudo groupadd $MONITORING_GROUP

# Grant sudo permission to the devops group
echo "%$DEVOPS_GROUP ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/$DEVOPS_GROUP

# Create users and add them to the devops group
for USERNAME in "${USERNAMES[@]}"; do
  sudo useradd -m -s /bin/bash $USERNAME
  echo "$USERNAME:$PASSWORD" | sudo chpasswd
  sudo usermod -aG $DEVOPS_GROUP $USERNAME

  # Create .ssh directory
  sudo mkdir -p /home/$USERNAME/.ssh
  sudo chown $USERNAME:$USERNAME /home/$USERNAME/.ssh
  sudo chmod 700 /home/$USERNAME/.ssh

  echo "User $USERNAME has been created, password set, and added to $DEVOPS_GROUP group."
done

echo "All users have been created and added to the $DEVOPS_GROUP group."
