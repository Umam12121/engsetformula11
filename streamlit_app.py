def export_pdf(data, fig):

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()
    elements = []

    # ================= COVER =================
    elements.append(Paragraph("LAPORAN SIMULASI SISTEM ENGSET", styles["Title"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(
        "Analisis Probabilitas Blocking pada Sistem Jaringan Telekomunikasi",
        styles["BodyText"]
    ))
    elements.append(Spacer(1, 20))


    # ================= INFORMASI UMUM =================
    elements.append(Paragraph("1. Informasi Sistem", styles["Heading2"]))
    elements.append(Spacer(1, 8))

    info = [
        ["Deskripsi", "Nilai"],
        ["Jumlah Source (S)", data["S"]],
        ["Jumlah Channel (N)", data["N"]],
        ["Traffic per Source (ρ)", data["rho"]],
        ["Traffic Idle (M)", f"{data['M']:.6f}"],
        ["Blocking Probability", f"{data['Pb']:.6f}"],
        ["Status Sistem", data["status"]],
        ["Jumlah Iterasi", data["iter"]],
        ["Waktu Simulasi", datetime.now().strftime("%d-%m-%Y %H:%M:%S")]
    ]

    table_info = Table(info)

    table_info.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1d4ed8")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.6, colors.grey),

        # 👉 FIX: RATA KIRI BIAR PROFESIONAL
        ("ALIGN", (0,0), (-1,-1), "LEFT"),

        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("PADDING", (0,0), (-1,-1), 6),
    ]))

    elements.append(table_info)
    elements.append(Spacer(1, 20))


    # ================= ITERASI =================
    elements.append(Paragraph("2. Tabel Iterasi Konvergensi", styles["Heading2"]))
    elements.append(Spacer(1, 8))

    iterasi = [["Iterasi", "M", "P(b)", "Selisih"]]
    iterasi += [[str(x) for x in row] for row in data["iter_data"]]

    table_iter = Table(iterasi)

    table_iter.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1d4ed8")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),

        ("ALIGN", (0,0), (-1,-1), "LEFT"),

        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 8),
    ]))

    elements.append(table_iter)
    elements.append(Spacer(1, 20))


    # ================= GRAFIK =================
    elements.append(Paragraph("3. Grafik Probabilitas Blocking", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    img = io.BytesIO()
    fig.savefig(img, format="png", dpi=220, bbox_inches="tight")
    img.seek(0)

    elements.append(Image(img, width=480, height=260))
    elements.append(Spacer(1, 20))


    # ================= KESIMPULAN =================
    elements.append(Paragraph("4. Kesimpulan", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    kesimpulan = f"""
    Berdasarkan hasil simulasi menggunakan model Engset,
    sistem menunjukkan kondisi <b>{data['status']}</b>.

    Nilai probabilitas blocking sebesar <b>{data['Pb']:.6f}</b>
    menunjukkan tingkat kepadatan trafik pada sistem.

    Hasil ini dapat digunakan sebagai dasar analisis kapasitas jaringan.
    """

    elements.append(Paragraph(kesimpulan, styles["BodyText"]))

    doc.build(elements)
    buffer.seek(0)

    return buffer
