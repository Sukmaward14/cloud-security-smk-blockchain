# cloud-security-smk-blockchain
Sistem keamanan dan verifikasi integritas dokumen administrasi SMK menggunakan Flask, SHA-256, Web3.py, Solidity, dan Blockchain Ganache.
# 🔐 Cloud Security & Blockchain - Verifikasi Dokumen Administrasi SMK

Sistem keamanan dokumen administrasi SMK berbasis **Flask, SHA-256, dan Blockchain** yang digunakan untuk membantu memeriksa integritas dokumen siswa.

Sistem melakukan verifikasi dengan membandingkan hash SHA-256 dokumen dengan hash yang tercatat pada smart contract blockchain.

---

## 👤 Identitas

**Nama:** Sukma Wardia Ningsih  
**NIM:** 105841112723  
**Program Studi:** Informatika  
**Semester:** 6  
**Mata Kuliah:** Cloud Security  
**Dosen Pengampu:** RUNAL REZKIAWAN, S.Kom., M.T  

---

## 🎯 Tujuan Sistem

Sistem ini dibuat untuk menerapkan konsep Cloud Security dan Blockchain pada proses pengelolaan serta verifikasi dokumen administrasi sekolah.

SHA-256 digunakan untuk menghasilkan sidik jari digital dari dokumen, sedangkan blockchain digunakan sebagai sumber data pembanding pada proses verifikasi.

---

## 🛠️ Teknologi yang Digunakan

- Python
- Flask
- SQLite
- SHA-256
- Web3.py
- Solidity
- Remix IDE
- Ganache
- HTML
- CSS

---

## ⛓️ Smart Contract

Smart contract yang digunakan adalah:

`DocumentRegistry.sol`

Smart contract menyimpan informasi berupa:

- Document ID
- Document Hash
- Timestamp
- Uploader Address

Fungsi utama smart contract:

### registerDocument()

Digunakan untuk mencatat ID dokumen dan hash SHA-256 dokumen ke blockchain.

### getDocument()

Digunakan untuk mengambil kembali informasi dokumen dari blockchain berdasarkan ID dokumen.

---

## 🔄 Alur Sistem

```text
Dokumen PDF
     ↓
Upload melalui Flask
     ↓
Perhitungan SHA-256
     ↓
Hash Dokumen
     ↓
DocumentRegistry Smart Contract
     ↓
Blockchain Ganache
     ↓
Verifikasi Dokumen
     ↓
Bandingkan Hash
     ↓
VALID / TIDAK VALID
