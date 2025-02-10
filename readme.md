## 🌟 Demo Purpose

This demo highlights the integration of **Generative AI** with **Cassandra 5.0.2** and **Langflow**, deployed on **Mission Control** (Azure VMs). The goal is to demonstrate how quickly a generative AI chatbot can be built to analyze and provide insights on transaction data, all within **under 10 minutes**.

---

## 🛠️ Environment and Deployment Notes

### **Infrastructure Setup**

1. **Azure VMs**:
    - **Control Plane**: `gmc-controlplane0`
    - **Platform Nodes**: `gmc-platform0`, `gmc-platform1`, `gmc-platform2`
    - **Database Nodes**: `gmc-database0`, `gmc-database1`, `gmc-database2`

2. **DNS Configuration**:
    - `gmc-controlplane0.eastus.cloudapp.azure.com`
    - `gmc-platform0.eastus.cloudapp.azure.com`

3. **Port Rules**:
    - **Port 8800**: Mission Control Kotsadm (`gmc-controlplane0`)
    - **Port 30880**: Mission Control Dashboard (`gmc-controlplane0`)
    - **Port 7860**: Langflow (`gmc-platform0`)

4. **Extra Disk**:
    - Add **128GB** to each VM.

### **Mission Control Installation**
- Run the installation commands for Mission Control as detailed in the [official guide](https://docs.datastax.com/en/mission-control/install/server-runtime.html).
- **Kotsadm Access**:
    - URL: `https://gmc-controlplane0.eastus.cloudapp.azure.com:8800/`
    - Default Password: `V9CnJu7U6`

### **Langflow Setup**
- Install **Docker**:
    ```bash
    sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```
- Run Langflow:
    ```bash
    docker run -it --rm -p 7860:7860 langflowai/langflow:latest
    ```
- **Langflow Dashboard**:  
  [Langflow](http://gmc-platform0.eastus.cloudapp.azure.com:7860)

---

## 🌐 Demo Browser Setup

- **Langflow**  
  [http://gmc-platform0.eastus.cloudapp.azure.com:7860](http://gmc-platform0.eastus.cloudapp.azure.com:7860)

- **Kotsadm for Mission Control**  
  [https://gmc-controlplane0.eastus.cloudapp.azure.com:8800/](https://gmc-controlplane0.eastus.cloudapp.azure.com:8800/)  
  **Password:** `V9CnJu7U6`

- **Mission Control Dashboard**  
  [https://gmc-controlplane0.eastus.cloudapp.azure.com:30880/](https://gmc-controlplane0.eastus.cloudapp.azure.com:30880/)  
  **Username:** `admin@example.com`  
  **Password:** `password`

- **External Chatbot Application**  
  [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## 🗃️ Database Schema Setup

## 📄 Sample Transactions CSV

```csv
Date,Account,Description,Category,Tags,Amount
12/31/2024,Credit Card 2637,Wendy's,Restaurants,,-25.92
12/31/2024,Checking 2637,American Express,Credit Card Payments,,-1300.38
12/31/2024,Checking 2300,Online Transfer To Person Two S Everyday Checking Xxxxxxxxx2628 Ref #ib0qs5vscv On 12/31/24,Transfers,,-50
```

### Create Keyspace:
```sql
CREATE KEYSPACE transactions_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
