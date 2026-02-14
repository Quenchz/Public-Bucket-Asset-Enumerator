# Public-Bucket-Asset-Enumerator
Multi-threaded asset discovery tool for enumerating publicly exposed storage bucket files using XML listings.

A multi-threaded Python tool designed to enumerate and discover publicly accessible files from storage bucket XML listings.
This tool helps security researchers and penetration testers identify exposed assets such as documents, images, and sensitive files.

 Features
- Multi-threaded scanning
- XML bucket parsing
- Automatic URL normalization
- Output saving support
- Error handling & status tracking
- Fast asset discovery
- Easy CLI usage


🛡️ Use Cases
- Public storage bucket enumeration
- Sensitive document discovery
- Bug bounty reconnaissance
- Asset exposure analysis


## ⚙️ Installation
Clone the repository:
```bash
git clone https://github.com/Quenchz/Public-Bucket-Asset-Enumerator.git
cd Public-Bucket-Asset-Enumerator
```

## 📦 Requirements
```bash
- Python 3.8+
- requests

Install dependencies:
pip install -r requirements.txt
```

## 🚀 Usage
```bash
### Basic Scan
python dircheck.py -u https://target-bucket.com -i bucket.xml
```

### Custom thread count & output name
```bash
python dircheck.py -u https://target-bucket.com -i bucket.xml -t 20 -o scan_result
```

## 🧾 Arguments
```bash
| Argument | Description |
|----------|------------|
| -u | Base bucket URL |
| -i | XML input file |
| -t | Thread count (default: 10) |
| -o | Output file prefix |
```

## 📂 Output
```bash
Results are saved inside the `output/` directory:

- result_200.txt → Accessible files
- result_403.txt → Forbidden files
- result_404.txt → Not found files
- result_errors.txt → Request errors
```

## 📸 Demo
```bash
![Tool Demo]
```
<img width="779" height="405" alt="demo" src="https://github.com/Quenchz/Public-Bucket-Asset-Enumerator/blob/main/demo.png" />

## ⚠️ Disclaimer
```bash
This tool is intended for:
- Educational purposes
- Authorized security testing
- Bug bounty research
- The developer is not responsible for misuse.
```


## 👨‍💻 Author
```
- Berkay Yaldız
- Cybersecurity Specialist / Pentester
```
