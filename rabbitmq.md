## Installing RabbitMQ on EC2 Ubuntu 20

### Step 1: Preparation

Before you start, ensure you have an EC2 instance running Ubuntu 20.04. Connect to your instance using SSH.

### Step 2: Create the Installation Script

Copy the provided installation script into a new file on your EC2 instance. You can use a text editor like `nano`:

```bash
nano install_rabbitmq.sh
```

Paste the script into the editor and save the file.

### Step 3: Give Execute Permissions

To make the script executable, run:

```bash
chmod +x install_rabbitmq.sh
```

### Step 4: Run the Installation Script

Execute the script to install RabbitMQ and its dependencies:

```bash
./install_rabbitmq.sh
```

Wait for the installation to complete.

---

## Configuring RabbitMQ

### Step 1: Access the RabbitMQ Management Console (Optional)

RabbitMQ comes with a built-in management console that you can enable:

```bash
sudo rabbitmq-plugins enable rabbitmq_management
```

Once enabled, you can access the management console by navigating to `http://your_ec2_ip:15672/`. The default login is `guest` for both the username and password.

### Step 2: Create a New User (Recommended)

For security reasons, it's a good idea to create a new user and give it the necessary permissions:

```bash
sudo rabbitmqctl add_user myuser mypassword
sudo rabbitmqctl set_user_tags myuser administrator
sudo rabbitmqctl set_permissions -p / myuser ".*" ".*" ".*"
```

Replace `myuser` and `mypassword` with your desired username and password.

---

## Managing RabbitMQ

- **Start RabbitMQ**:

  ```bash
  sudo systemctl start rabbitmq-server
  ```

- **Stop RabbitMQ**:

  ```bash
  sudo systemctl stop rabbitmq-server
  ```

- **Restart RabbitMQ**:

  ```bash
  sudo systemctl restart rabbitmq-server
  ```

- **Check RabbitMQ Status**:

  ```bash
  sudo systemctl status rabbitmq-server
  ```

---

That's it! You've successfully installed, configured, and learned how to manage RabbitMQ on your EC2 Ubuntu 20 instance.
