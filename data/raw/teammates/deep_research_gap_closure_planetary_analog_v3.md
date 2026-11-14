---
title: Deep Research - Penutupan Celah Laporan Validasi v2
tags: nasa-space-apps, validation, planetary-analog, artemis, mars
description: Jawaban atas butir yang belum terjawab di validation_report_planetary_analog_v2.md
---

# 🔬 Deep Research v3: Penutupan Celah Laporan Validasi
### Planetary Analog Campaign Architect, NASA Space Apps 2026

**Tanggal riset:** 14 November 2026
**Dasar:** `validation_report_planetary_analog_v2.md`, Bagian 0.2, 1, 3.2, 3.3, 5.2, 9. Hanya butir berstatus 🟠/🔴 yang dikerjakan di sini.

## 0. Ringkasan Eksekutif

### 0.1 Legenda status bukti (sama dengan v2)

| Kode | Arti |
|---|---|
| ✅ **A** | Diverifikasi ke sumber primer / rilis resmi / abstrak jurnal saat riset ini dilakukan |
| 🔵 **B** | Diverifikasi ke sumber sekunder (berita, ringkasan, preprint), perlu dicek ke sumber primer |
| 🟠 **C** | Dari ingatan atau sumber yang tidak bisa dibuka penuh, belum diverifikasi |
| 🔴 **D** | Hitungan kasar internal, **jangan dikutip sebagai fakta** |

### 0.2 Status butir setelah riset ini

| Butir v2 | Status v2 | Status sekarang | Catatan |
|---|---|---|---|
| Referensi tingkat C (Bagian 3.2) | 🟠 | 🟢 **7 dari 8 terverifikasi** | Pengecualian: persamaan Bekker-Wong (butuh buku) |
| Profil lava tube Mars | 🔴 | 🟠 | Skala dan morfologi terisi; **suhu interior Mars dan radiasi GCR di dalam tube masih kosong** |
| Profil Jezero | 🔴 | 🟠 | Suhu tanah, inersia termal, angin, debu terisi; **tekanan MEDA-PS dan batuan belum** |
| Profil kutub Bulan | 🔴 | 🟠 | Regolit dan termal in-situ terisi; **kemiringan/kekasaran per wilayah belum** |
| Debu dan atmosfer (Bagian 5.2) | 🔴 | 🟠 | Debu Mars, angin Jezero, debu Bulan terisi; **kelembapan Mars belum** |
| Konveksi Mars (hitungan nyata) | 🔴 D | 🔴 D (sudah dihitung) | Hasil orde besar, properti gas dari ingatan |
| Literatur analog (Bagian 3.3) | 🔴 | 🟠 | HMP, Atacama, Islandia terisi; **Indonesia hampir kosong** |
| Status Artemis | ✅/🔵 | ✅ diperbarui | Artemis IV 2028 kini ✅ A |
| Isi kolom "Bukti" register failure mode | 🔴 | 🟠 | 10 dari 17 baris terisi (Bagian 7) |
| **P1: uji rediscovery** | 🔴 | 🔴 **tidak bisa diselesaikan lewat riset** | Butuh dataset dan eksekusi model (Bagian 9) |

### 0.3 Temuan baru yang mengubah laporan v2

:::danger
Tiga hal ini wajib dibawa ke slide dan skrip pitch.
:::

| # | Temuan | Dampak |
|---|---|---|
| N1 | **UNSCEAR terbaru (2026)** menaikkan rata-rata global dosis alami dari 2,4 menjadi sekitar **3,0 mSv/tahun**. Kenaikan ini dari perbaikan data dan metode, bukan radiasi naik | Angka "2,4 mSv/tahun" di v2 sudah usang. Pakai ~3,0 mSv/tahun dan sebut UNSCEAR 2026 (✅ A, siaran pers UN) |
| N2 | Selisih suhu **permukaan tanah** Jezero ternyata sekitar **88 K** (−83 °C menjelang fajar sampai +5 °C siang). Selisih udara 50-60 K (K3 di v2) tetap benar untuk udara | Draf awal "80-100 K" kemungkinan merujuk ke suhu tanah. **Jangan hapus mentah-mentah**: bedakan udara vs tanah di slide |
| N3 | Jezero adalah lokasi dengan **aktivitas angkat debu tertinggi** yang pernah tercatat misi permukaan Mars. Sensor angin MEDA rusak oleh pasir | Panel surya di Jezero mungkin justru dapat "pembersihan alami". Jangan generalisasi laju degradasi 0,2%/sol ke semua lokasi |

---

## 1. Referensi tingkat C yang kini terverifikasi (menjawab Bagian 3.2)

| Referensi | Hasil verifikasi | Status | Sumber |
|---|---|---|---|
| Massa Perseverance 1.025 kg | **Benar.** JPL: ~1.025 kg (2.260 lb) | ✅ A | JPL press kit, *Mars 2020 quick facts*: https://www.jpl.nasa.gov/news/press_kits/mars_2020/launch/quick_facts/ |
| Berat dan massa uji setara | W = 1.025 × 3,71 = **3.803 N**; massa uji = **387,6 kg** | ✅ aritmetika | Hitungan Bagian 8 |
| Fluks surya Mars ~590 W/m² | **Rata-rata 586-589 W/m²** (lembar fakta NASA). Rentang: **~490 W/m² (aphelion) sampai ~713 W/m² (perihelion)**, dihitung dari 1361/r² dengan r = 1,666 dan 1,381 AU. **Koreksi:** batas atas "720" sebaiknya 713 | ✅ A (rata-rata), ✅ hitungan (rentang) | NASA Planetary Fact Sheet: https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html |
| Tekanan permukaan Mars | Rata-rata global **~610 Pa (≈6,1 mbar)**; rentang musiman **4,0-8,7 mbar** menurut versi lembar fakta NASA yang saya baca. v2 menulis "6 mbar (3-9)": cukup dekat, tapi rentang resmi 4,0-8,7 | 🔵 B (arsip lembar fakta) | Arsip NASA NSSDC: https://webarchive.library.unt.edu/eot2008/20090118195415/http://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html |
| **UNSCEAR dosis alami** | 2,4 mSv/tahun (UNSCEAR 2008) **digantikan ~3,0 mSv/tahun** (UNSCEAR 2026) | ✅ A (siaran pers) | https://unis.unvienna.org/unis/en/pressrels/2026/unisous453.html |
| **ESCC 22900** | *Total Dose Steady-State Irradiation Test Method*, Issue 4, Okt 2010. Mencakup uji dosis total dan kerusakan displacement dengan sumber Co-60/elektron | ✅ A | ESCIES: https://escies.org/download/specdraftapppub?id=29 |
| **ESCC 25100** | *Single Event Effects Test Method and Guidelines* | ✅ A | Daftar rujukan ESCC: https://escies.org/download/specdraftapppub?id=2798 |
| **MIL-STD-883 TM1019** | *Ionizing Radiation (Total Dose) Test Procedure* untuk mikrosirkuit. Pasangan Eropanya adalah ESCC 22900. Untuk SEE, acuan tambahan: **JESD57** dan **ASTM F1192** | ✅ A | Makalah OSTI: https://www.osti.gov/servlets/purl/1268236 |
| **Hukum Paschen CO₂** | Untuk gas campuran Mars, tegangan tembus minimum terukur **410 ± 10 V pada 0,3 Torr·cm**. Pada ~5,2 Torr itu setara celah **~0,6 mm** (hitungan sendiri). Pada 7 mbar, celah 5 mm tembus pada **725 V** dan 10 mm pada **895 V**. Minimum Paschen CO₂ jatuh di rentang tekanan permukaan Mars. Campuran <0,1% gas lain dapat mengubah kurva | ✅ A (abstrak) | *Adv. Space Res.* 2010, "Electric discharge in the Martian atmosphere, Paschen curves and implications for future missions"; NASA NTRS 20030110694 (Buhler); NASA NTRS 20110015825 |
| **Indeks aridity UNEP** | AI = P / PET. Kelas: **<0,03 hyper-arid; 0,03-0,2 arid; 0,2-0,5 semi-arid; 0,5-0,65 dry sub-humid; >0,65 humid**. Dataset: *Global-AI_PET_v3*, resolusi 30 detik busur (~1 km), periode 1970-2000, PET dari FAO-56 Penman-Monteith, lisensi CC BY 4.0 | ✅ A | Zomer, Xu & Trabucco (2022), *Sci. Data* 9:409, doi:10.1038/s41597-022-01493-1 |
| **Coffin-Manson m ≈ 2** | **Bergantung konvensi.** Eksponen ΔT pada faktor akselerasi Norris-Landzberg untuk SnPb ≈ **1,9**; sumber lain memakai **2,4-2,5** untuk Sn/Pb. Untuk SAC305 ada ajuan eksponen kelelahan ~1,96. Konstanta SnPb **tidak boleh dipakai langsung untuk SAC** (selisih bisa 2-3×) | 🔵 B | Ringkasan Norris-Landzberg (metricgate.com, accendoreliability.com); makalah SMTA: https://journal.smta.org/index.php/smt/article/download/68/36/500 |
| **Bekker-Wong** | **Tidak diverifikasi.** Persamaan harus diambil dari Wong, *Theory of Ground Vehicles* | 🟠 C | Tetap tindakan manual |

:::warning
**Catatan Coffin-Manson:** tulis rumus dan konvensinya di slide. "Eksponen 2" di faktor akselerasi `AF = (ΔT_uji/ΔT_lapangan)^m` bukan eksponen yang sama dengan `Nf = C·Δε_p^(-n)`. Mencampurnya adalah kesalahan umum.
:::

---

## 2. Lava tube Mars (menjawab Bagian 1.3)

**Status: 🟠.** Skala, morfologi, dan lokasi kandidat sudah ada. Fisika interior Mars belum terverifikasi.

| Parameter | Nilai | Status | Sumber |
|---|---|---|---|
| Ukuran relatif | Tube Mars dan Bulan **1 sampai 3 orde besar lebih voluminer** daripada tube Bumi. Siaran pers Univ. Bologna menyebut Mars ~100× dan Bulan ~1.000× lebih lebar | ✅ A (abstrak) / 🔵 B (angka lebar) | Sauro et al. (2020), *Earth-Science Reviews* 209:103288, doi:10.1016/j.earscirev.2020.103288 |
| Alasan lebih besar dan tetap stabil | Gravitasi rendah mengurangi gaya yang meruntuhkan atap | 🔵 B | Liputan atas Sauro 2020 |
| Bukti keberadaan di Mars | Rantai runtuh dan **skylight** pada aliran lava; belum ada tube Mars yang dieksplorasi langsung | ✅ A / 🔵 B | Sauro 2020; NSS ltube96 |
| Lokasi kandidat | Arsia Mons (tujuh skylight terlihat di THEMIS), Olympus Mons sisi barat, Alba Patera, Hadriacus Mons (kandidat tube dari ~1.500 citra MRO, preprint) | 🔵 B | arXiv 2302.09006; arXiv 2004.13156 |
| Skylight bukan tempat huni | Habitat sebaiknya **jauh dari skylight** karena atap di sana rapuh dan radiasi lebih tinggi | 🔵 B | ISU ACCESS Mars (2009) |
| Perisai UV | Pit crater dan skylight Mars secara efektif menahan UV permukaan | ✅ A (abstrak) | *Icarus* (2021), doi via ScienceDirect S0019103521003171 |
| Perisai radiasi | Pada **tube analog di Bumi**, dosis dalam turun ~82% (0,470 → 0,083 µSv/jam). **Ini radiasi lingkungan Bumi, bukan GCR Mars.** Preprint yang memproyeksikan 342 → ~62 µSv/hari untuk Mars adalah ekstrapolasi, bukan pengukuran | 🔴 **jangan dikutip sebagai fakta Mars** | Paris et al., arXiv 2004.13156 (preprint) |
| Suhu interior tube Mars | **Tidak ditemukan sumber terverifikasi.** Satu-satunya angka stabil (~17 °C) adalah pit **Bulan** (Horvath 2022) | 🔴 | n/a |

**Implikasi untuk aplikasi:** kartu lava tube cukup menyatakan *"secara prinsip melindungi UV, partikel, dan ayunan suhu; belum dikuantifikasi untuk Mars"*. Model lima variabel remote-sensing tidak menangkap atap, lubang masuk, atau komunikasi (FM-17).

---

## 3. Profil Jezero (menjawab Bagian 1.2)

| Parameter | Nilai | Status | Sumber |
|---|---|---|---|
| Suhu **tanah** tipikal | Sekitar **−83 °C (pra-fajar) sampai +5 °C (siang)**, selisih ≈ **88 K** | 🔵 B | Munguira (JPL blog), SpaceDaily: https://www.spacedaily.com/reports/Daily_records_of_atmospheric_temperature_with_Perseverance_999.html |
| Suhu **udara** tipikal | −83 °C sampai −23 °C | 🔵 B | idem |
| Inersia termal permukaan | **180 (bukit pasir) sampai 605 (batuan dasar)** J m⁻² K⁻¹ s⁻½; rata-rata sepanjang rute **~350** (MEDA), **~330** (THEMIS) | ✅ A (abstrak) | Martínez et al. (2023), *JGR Planets*, doi:10.1029/2022JE007537 |
| Albedo | Non-Lambertian; terendah saat tengah hari. Cocok dengan retrieval orbital | ✅ A (abstrak) | idem |
| Konveksi harian | Fluktuasi suhu udara memuncak saat siang, tipikal **2,5 K pada 1,45 m**; inversi malam **patah** di medan inersia tinggi | ✅ A (abstrak) | Munguira et al. (2023), *JGR Planets* 128:e2022JE007559 |
| Dust devil | Jezero memiliki **kelimpahan dust devil tertinggi** yang pernah terdeteksi misi permukaan. Penurunan tekanan **0,3-6,5 Pa**, durasi **1-200 s**, diameter **5-135 m**, kecepatan rotasi **~4-24 m/s** | ✅ A (abstrak) | Rodríguez-Manfredi et al. (2023), *Nat. Geosci.* 16:19-28 |
| Badai debu lokal (Jan 2022) | Kedalaman optik visual puncak **~2**; angin hingga **20 m/s** sebelum sensor angin rusak; 21 peristiwa pengangkat debu dalam 25 menit | ✅ A | Lemmon et al. (2022), *GRL*, doi:10.1029/2022GL100126 |
| Radiasi | Pengukuran 0,67 mSv/hari ada di **Gale**, bukan Jezero. Tidak ada angka dosis Jezero terverifikasi | 🔴 | Hassler 2014 |
| Tekanan MEDA-PS | **Angka tidak berhasil diekstrak** (halaman jurnal diblokir). Yang terkonfirmasi: sensor bekerja baik pada 530 sol pertama; variasi harian ada | 🟠 C | Rodríguez-Manfredi 2023 |
| Jenis batuan, distribusi batu | **Belum diriset** | 🔴 | HiRISE/CTX/Mars 2020 |

**Koreksi:** pernyataan v2 "selisih siang-malam udara 50-60 K" tetap valid untuk udara. Tambahkan baris suhu tanah (~88 K) agar subsistem termal dan roda tidak memakai angka udara.

---

## 4. Profil Kutub Selatan Bulan (menjawab Bagian 1.1)

### 4.1 Status misi dan wilayah (✅ A, diperbarui)

| Fakta | Nilai | Sumber |
|---|---|---|
| Pendaratan awak pertama | **Artemis IV, target 2028** (awal 2028 menurut briefing HLS) | NASA: https://www.nasa.gov/missions/artemis/nasa-shares-plans-to-accelerate-artemis-return-to-moon/ |
| Artemis III | Uji **orbit rendah Bumi**, 2027 (target Q3 2027), uji docking dengan lander SpaceX dan Blue Origin, 14 hari, 4 astronot | NASA (sama) |
| Risiko jadwal | Audit OIG NASA menilai pendaratan aman bisa mundur ke ~2030-2031. Memo internal Sept 2026 menyebut Artemis III ~90 hari terlambat | 🔵 B: *Nuclear Engineering International*, 30 Okt 2026 |
| Artemis II | Terbang **April 2026**, penerbangan lintas Bulan berawak | 🔵 B (Wikipedia) |
| Gateway | Dilaporkan dibatalkan Maret 2026 | 🔵 B (Wikipedia) |
| Wilayah kandidat | **13 wilayah** (Agu 2022), diperkecil menjadi **9 wilayah** (Okt 2024): Peak near Cabeus B, Haworth, Malapert Massif, Mons Mouton Plateau, Mons Mouton, Nobile Rim 1, Nobile Rim 2, de Gerlache Rim 2, Slater Plain | ✅ A: https://www.nasa.gov/news-release/nasa-provides-update-on-artemis-iii-moon-landing-regions/ |
| Ukuran wilayah | Tiap wilayah ~15 × 15 km; **lokasi** pendaratan berjari-jari ~100 m | 🔵 B (Fox Weather) |

:::warning
**Belum terverifikasi:** apakah daftar 9 wilayah (disusun untuk Artemis III lama) masih menjadi daftar Artemis IV setelah restrukturisasi Februari 2026. Sumber yang saya baca tidak menyebut wilayah Artemis IV. Beri label "daftar 2024".
:::

### 4.2 Regolit (menjawab "belum diriset")

| Parameter | Nilai | Status | Sumber |
|---|---|---|---|
| Kohesi, Apollo (dekat permukaan) | **0,1-1,0 kPa** | ✅ A | Ringkasan di *Research* (2026), DOI 10.34133/research.1064 |
| Sudut gesek, Apollo | **30°-50°** | ✅ A | idem |
| Surveyor 3 dan 7 | c = 0,35-0,7 kPa; φ = 35°-37° | ✅ A | idem |
| Kepadatan massa | **~1,30 g/cm³ di permukaan → ~1,92 g/cm³ di bawah 100 cm**; kohesi naik melewati 3 kPa di bawah ~50 cm | ✅ A (abstrak NASA) | Connolly & Carrier, LPSC 2023: https://ntrs.nasa.gov/api/citations/20220018853/downloads/LPSC%202023%20Abstract_Connolly_Carrier_v2.pdf |
| Chang'e-6 (sisi jauh, SPA) | c ≈ 1,08 kPa; φ ≈ 48° (simulasi DEM). **Bukan data kutub** | 🔵 B | *Research* (2026) |
| In-situ dekat kutub (69°S, Chandrayaan-3) | Lapisan atas **2-6 cm sangat berpori tetapi kohesif**, lalu lapisan padat ("kue berlapis"). Suhu permukaan **~50-70 °C** vs **~−10 °C pada 8-10 cm** (angka bervariasi antar laporan) | 🔵 B | ISRO/PRL via PIB dan liputan |
| Pengaruh es di PSR | Kohesi dan sudut gesek akan berubah bila ada es; belum terukur | 🔴 | n/a |

**Implikasi:** pustaka regolit ada, tetapi **tidak ada pengukuran geoteknik di dalam 9 wilayah**. Nilai di atas hanya rentang Apollo (lintang rendah) dan satu titik 69°S. Tanah kohesif dan berlapis memperlemah argumen bahwa efek gravitasi pada tanah bisa dikalibrasi dengan hasil simulan GRC-1 (Bagian 4.5 v2).

### 4.3 Yang masih kosong

Kemiringan, kekasaran, dan distribusi batu per wilayah (LOLA/LROC) **belum diriset**. Itu tugas pengolahan data, bukan pencarian literatur.

---

## 5. Debu dan atmosfer (menjawab Bagian 5.2)

### 5.1 Mars

| Aspek | Nilai | Status | Sumber |
|---|---|---|---|
| Degradasi panel surya oleh debu | **~0,2% per sol tipikal**, rentang **0,05-2% per sol** (Pathfinder, Phoenix, InSight, Spirit, Opportunity) | ✅ A (abstrak) | Lorenz et al. (2021), *Planet. Space Sci.* 207 |
| Pembersihan alami | Spirit dan Opportunity sering "dibersihkan" dust devil dan hembusan; InSight tidak (tanpa dust devil terdeteksi). Frekuensi **bergantung lokasi** | ✅ A | idem |
| Implikasi Jezero | Aktivitas angkat debu tinggi; pembersihan alami mungkin, tapi **belum ada data panel surya di Jezero** (Perseverance bertenaga RTG) | 🔵 B | NASA/JPL: *Perseverance Studies the Wild Winds of Jezero* |
| Badai debu | Jezero Jan 2022: τ ≈ 2, angin hingga 20 m/s, sedimen termobilisasi dan menimbun dek rover | ✅ A | Lemmon 2022 |
| Dust devil | Lihat Bagian 3 | ✅ A | Rodríguez-Manfredi 2023 |
| Kelembapan relatif | Model Savijärvi memakai RH udara 40-90% menjelang fajar. **Ini keluaran model, bukan pengukuran terverifikasi** | 🟠 C | Savijärvi et al. (2023) |

### 5.2 Bulan

| Aspek | Temuan | Status | Sumber |
|---|---|---|---|
| Sembilan kategori masalah debu Apollo | Obskurasi penglihatan, pembacaan instrumen palsu, pelapisan/kontaminasi, hilang traksi, **penyumbatan mekanisme**, **abrasi**, masalah termal, **kegagalan segel**, iritasi hirup | ✅ A | Gaier (2005), NASA/TM-2005-213610 |
| Segel | Semua segel lingkungan, gas, dan sampel regolit Apollo gagal | ✅ A (slide Gaier) | Gaier & Creel (2005) |
| Termal | Baterai LRV melewati batas suhu karena debu menutup radiator | ✅ A (slide Gaier) | idem |
| Uji Bumi meremehkan | Tingkat keparahan **secara konsisten diremehkan** oleh uji darat | ✅ A | Gaier 2005 |
| Adhesi di vakum | Adhesi elektrostatik naik dengan kebersihan material, kadang >10×; simulasi Bumi tidak memprediksi besarnya | ✅ A | Berkebile & Gaier (2012), NASA/TM-2012-217723 |
| Mekanisme alami | Transpor debu alami tidak signifikan dalam 14 hari; **mekanisme antropogenik** (berjalan, roda, plume roket) dominan | ✅ A | Gaier 2005 |

**Implikasi:** FM-16 dan FM-09 mendapat bukti kuat ✅. Pernyataan "simulan Bumi kurang mewakili debu Bulan" kini punya sitasi NASA langsung.

---

## 6. Konveksi Mars: hitungan nyata (menjawab P3)

**Status: 🔴 D.** Properti gas diambil dari ingatan (🟠 C). Hasil ini orde besar, bukan simulasi CFD.

**Kasus:** kotak elektronik 20 cm, ΔT dinding-udara 30 K, konveksi alami pada dinding vertikal (korelasi Churchill-Chu), emisivitas 0,8.

| | Bumi (293 K, 1 atm) | Mars (220 K, 700 Pa) |
|---|---|---|
| Kerapatan udara | 1,205 kg/m³ | 0,0168 kg/m³ |
| Bilangan Rayleigh | 2,5 × 10⁷ | **6,9 × 10³** |
| Bilangan Nusselt | ~41 | ~5,0 |
| Koefisien konveksi h | ~5,2 W/m²K | **~0,28 W/m²K** |
| Radiasi linear (250 K, ε=0,8) | ~2,8 W/m²K | ~2,8 W/m²K |

**Hasil:**
- Ra Mars sekitar **4 orde besar lebih kecil** (rasio 2,8 × 10⁻⁴), karena Ra ∝ g·ρ² dan kerapatan turun ~70×.
- Konveksi Mars ≈ **0,28 W/m²K**, sekitar **10× lebih kecil dari radiasi** pada kondisi yang sama. **Pendinginan komponen di Mars didominasi radiasi dan konduksi.**
- Sensitivitas tekanan (400-870 Pa): Nu 4,0-5,5. Hasil tidak sensitif terhadap rentang tekanan musiman.
- Bila terhitung h ≈ 0,3 W/m²K, 30 K × 0,3 ≈ **9 W/m²** diangkat konveksi, kecil dibanding fluks surya (~490-713 W/m² di luar atmosfer).

**Kelemahan yang harus disebut:** korelasi dipakai di luar rentang validasinya (Nu rendah); aliran Mars di Jezero dipengaruhi turbulensi sekitar (angin 2 m/s malam, dust devil), sehingga konveksi paksa bisa mengalahkan konveksi alami. **Jangan dikutip sebagai fakta.**

---

## 7. Register failure mode: kolom "Bukti" yang kini terisi

| ID | Failure mode | Bukti baru | Status |
|---|---|---|---|
| FM-05 | Gagal mendeteksi bahaya (bayangan) | Williams et al. 2019 (sudut matahari 1,54°) | ✅ A (sudah ada di v2) |
| FM-09 | Penurunan daya panel oleh debu | Lorenz 2021: 0,2%/sol (0,05-2%); pembersihan bergantung lokasi | ✅ A |
| FM-11 | Kelelahan siklus termal | Diviner (selisih ~300 K), Coffin-Manson (eksponen bergantung alloy) | 🔵 B |
| FM-12 | Pemanas malam / PSR | Diviner: PSR 25-110 K; ChaSTE: gradien 60-70 K dalam 10 cm | ✅ A / 🔵 B |
| FM-13 | Overheating (konveksi hilang) | Hitungan Bagian 6 (h ≈ 0,28 vs radiasi ≈ 2,8 W/m²K) | 🔴 D |
| FM-14 | Tembus listrik di CO₂ | 410 ± 10 V pada 0,3 Torr·cm; 725 V (celah 5 mm, 7 mbar) | ✅ A (abstrak) |
| FM-15 | SEE / TID | ESCC 22900, ESCC 25100, MIL-STD-883 TM1019, JESD57, ASTM F1192; dosis di v2 | ✅ A |
| FM-16 | Abrasi segel oleh regolit | Gaier 2005: abrasi dan kegagalan segel Apollo | ✅ A |
| FM-17 | Lava tube / skylight | Sauro 2020 (ukuran); ISU 2009 (jauhi skylight) | 🔵 B |
| FM-04 | Kerusakan roda oleh batuan | **Belum dicari** | 🔴 |
| FM-06 | Visual odometry gagal | **Belum dicari** | 🔴 |
| FM-07, 08 | Bor | **Belum dicari** | 🔴 |

---

## 8. Hitungan yang bisa diverifikasi ulang (✅ aritmetika)

| Besaran | Hasil |
|---|---|
| Berat Perseverance di Mars | 3.803 N |
| Massa uji setara (Mars) | 387,6 kg |
| Rover 400 kg di Bulan: berat; massa uji | 648 N; 66,1 kg |
| Percepatan relatif pada gaya sama | Mars 2,64×; Bulan 6,06× |
| Dosis Mars 0,67 mSv/hari | ≈ 245 mSv/tahun |
| Dosis Bulan 60 µSv/jam | ≈ 1,44 mSv/hari **siang**; 14 hari siang ≈ 20 mSv |
| Fluks surya Mars | perihelion ~713; aphelion ~490 W/m² |
| Celah Paschen minimum | 0,3 Torr·cm ÷ 5,2 Torr ≈ 0,58 mm |

---

## 9. Literatur analog dan situs acuan (menjawab Bagian 3.3)

### 9.1 Situs acuan yang punya sitasi

| Situs | Alasan keilmuan | Status | Sumber |
|---|---|---|---|
| **Haughton (Devon Island, Kanada)** | Satu-satunya struktur tumbukan di gurun kutub; permafrost kontinu; kawah ~23 km (rim ~16 km); analog bentuk lahan Mars (periglasial, lembah, gully) | ✅ A | Lee & Osinski (2005), *Meteorit. Planet. Sci.* 40:1755 |
| **Atacama, inti hiper-arid (Yungay)** | Tanah "mirip Mars" (organik sangat rendah, bakteri kultivasi sangat sedikit, oksidan), hujan sekali dalam beberapa tahun, UV tertinggi di Bumi | ✅ A | Navarro-González et al. (2003), *Science* 302:1018; Azua-Bustos et al. (2022), *Front. Astron. Space Sci.* 8:810426 |
| Atacama, María Elena Sur | Lokasi yang dilaporkan lebih kering dari Yungay (RH rata-rata 17,3% vs 28,8%) | 🔵 B | Ringkasan atas Azua-Bustos et al. |
| **Islandia (Askja, Mývatn, Krafla)** | Pelatihan geologi astronot Apollo, Juli **1965** dan Juli **1967**; "paling mirip Bulan" menurut dokumen NASA; sembilan dari 12 pejalan Bulan ikut salah satunya; basalt dan pasir basal dipakai menguji rover Mars 2020 | 🔵 B | Exploration Museum; Wikipedia *Apollo program training*; AFP/phys.org (2019) |
| McMurdo Dry Valleys (Antartika) | Dikatakan paling mirip Mars dalam katalog analog ESA | 🔵 B (liputan BBVA) | Perlu cek langsung ke katalog ESA |

:::warning
**Peringatan sirkularitas (Bagian 8.2 v2):** daftar di atas disusun dari kebutuhan analog (dari literatur), bukan dari hasil model. Tetap dokumentasikan alasan pemilihan sebelum menjalankan model.
:::

### 9.2 Indonesia

| Pernyataan | Hasil | Status |
|---|---|---|
| Studi analog planet peer-reviewed di **Tengger/Bromo** | **Tidak ditemukan.** Hanya ada geokimia dan pemantauan gunung api | 🔴 |
| Studi analog di **Gunung Sewu** dan **Maros-Pangkep** | **Tidak dicari spesifik** pada sesi ini | 🔴 (belum dicari) |
| "Permafrost Indonesia" | **Tidak ada dukungan.** Es di Indonesia hanya di **Puncak Jaya (4.884 m)**: luas **~0,09 km² (Sept 2025)** dari ~19,3 km² (1850); BMKG memproyeksikan hilang **2026-2027**, studi lain **~2030**; ekspedisi 2026 menemukan East Northwall Firn bertahan melewati prediksi lama | ✅ A (BMKG via Arab News) / 🔵 B |
| Implikasi | **Hapus klaim permafrost Indonesia**. Kaldera Indonesia hanya bisa disebut **analog medan vulkanik dan abu**, dengan catatan tropis lembap dan bervegetasi | 🟠 usulan |

---

## 10. Yang masih belum bisa dijawab dari riset

| Butir | Alasan | Langkah |
|---|---|---|
| **P1: uji rediscovery** | Butuh data (LOLA, MOLA, NASADEM, MODIS, Global-AI v3) dan eksekusi model. Sandbox ini **tanpa akses jaringan**, jadi dataset tidak bisa diunduh di sini | Jalankan di mesin tim; gunakan protokol Bagian 8.2 v2 |
| Suhu dan radiasi interior lava tube Mars | Tidak ada sumber terverifikasi | Cari Williams et al. (*Icarus*, stabilitas termal gua Mars) dan studi GCR dalam gua |
| Tekanan MEDA-PS Jezero | Halaman jurnal diblokir | Ambil dari PDS atau Rodríguez-Manfredi 2023 langsung |
| Batuan Jezero; kemiringan 9 wilayah kutub | Tugas olah data | HiRISE/CTX; LOLA/LROC |
| Efek gravitasi pada **tanah kohesif** (GSL) | Tidak dicari | Cari studi regolit kohesif dan parabolic flight terbaru |
| Karst Indonesia sebagai analog | Tidak dicari | Cari literatur speleologi dan analog gua |
| FM-04, 06, 07, 08 | Tidak dicari | Isi kolom Bukti |

### Tidak boleh diklaim sekarang

- ❌ "Model kami menemukan kembali Atacama/Haughton/Islandia di top 5%."
- ❌ "Tube lava Mars mengurangi radiasi 82%." (data analog Bumi, preprint)
- ❌ "Panel surya di Jezero akan terdegradasi 0,2% per sol." (laju rata-rata antar-lokasi)
- ❌ "Konveksi Mars lebih lemah X kali." (hitungan 🔴 D)
- ❌ "Indonesia punya permafrost."

### Aman diucapkan sekarang

- ✅ "Pendaratan awak di Bulan kini ditargetkan Artemis IV (2028); Artemis III adalah uji orbit rendah Bumi."
- ✅ "Uji darat meremehkan tingkat keparahan debu Bulan; segel Apollo semuanya gagal." (Gaier 2005)
- ✅ "Panel surya Mars kehilangan rata-rata ~0,2% per sol, 0,05-2% bergantung lokasi." (Lorenz 2021)
- ✅ "Di CO₂ pada tekanan Mars, tegangan tembus minimum terukur ~410 V; busur lebih mudah terjadi." (Paschen)
- ✅ "Jezero punya dust devil terbanyak yang pernah tercatat di permukaan Mars." (Rodríguez-Manfredi 2023)

---

## Lampiran. Daftar sumber dalam riset ini

**Misi dan program:** NASA (nasa.gov/missions/artemis/nasa-shares-plans-to-accelerate-artemis-return-to-moon); NASA (nasa.gov/news-release/nasa-provides-update-on-artemis-iii-moon-landing-regions); Nuclear Engineering International; Congress.gov CRS IF11643.
**Jezero:** Rodríguez-Manfredi 2023; Martínez 2023 (doi:10.1029/2022JE007537); Munguira 2023 (doi:10.1029/2022JE007559); Lemmon 2022 (doi:10.1029/2022GL100126); Savijärvi 2023.
**Lava tube:** Sauro 2020 (doi:10.1016/j.earscirev.2020.103288); ISU ACCESS Mars 2009; Paris et al. arXiv 2004.13156; *Icarus* 2021 (ScienceDirect S0019103521003171); Losarcos & Dombard 2025, *Space Sci. Rev.* 221:127.
**Regolit dan debu Bulan:** Connolly & Carrier LPSC 2023; *Research* 2026 (10.34133/research.1064); Gaier 2005; Berkebile & Gaier 2012; Gasteiner et al. 2026 (database regolit, arXiv 2602.03829).
**Debu Mars:** Lorenz et al. 2021, *Planet. Space Sci.* 207.
**Paschen:** *Adv. Space Res.* 2010; NASA NTRS 20030110694, 20110015825.
**Standar:** ESCC 22900, 25100; MIL-STD-883 TM1019 (OSTI 1268236).
**Dosis:** UNSCEAR 2026 (unis.unvienna.org); CNSC fact sheet (UNSCEAR 2008).
**Aridity:** Zomer et al. 2022, *Sci. Data* 9:409.
**Analog:** Lee & Osinski 2005; Navarro-González 2003; Azua-Bustos 2022; Exploration Museum; BMKG/Arab News; Project Pressure (2026).
