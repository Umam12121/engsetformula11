def export_pdf(data, fig):

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()
    elements = []

    # =========================================================
    # COVER REPORT (PROFESSIONAL)
    # =========================================================
    elements.append(Paragraph("LAPORAN SIMULASI ENGSETPRO", styles["Title"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(
        "Analisis Probabilitas Blocking pada Sistem Engset",
        styles["BodyText"]
    ))

    elements.append(Spacer(1, 20))


    # =========================================================
    # INFORMASI SISTEM (RAPI TABLE - FIX UTAMA)
    # =========================================================
    elements.append(Paragraph("1. Parameter Sistem", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    param_data = [
        ["Parameter", "Nilai"],
        ["Jumlah Source (S)", data["S"]],
        ["Jumlah Channel (N)", data["N"]],
        ["Traffic per Source (ρ)", data["rho"]],
        ["Traffic Idle (M)", f"{data['M']:.6f}"],
        ["Blocking Probability", f"{data['Pb']:.6f}"],
        ["Status Sistem", data["status"]],
        ["Jumlah Iterasi", data["iter"]],
        ["Waktu Simulasi", data.get("time", "-")]
    ]

    table_param = Table(param_data)

    table_param.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1d4ed8")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.6, colors.grey),

        # 👉 RATA KIRI BIAR TEKNIS & ENAK DIBACA
        ("ALIGN", (0,0), (-1,-1), "LEFT"),

        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("PADDING", (0,0), (-1,-1), 6),
    ]))

    elements.append(table_param)
    elements.append(Spacer(1, 20))


    # =========================================================
    # ITERATION TABLE (TETAP LENGKAP)
    # =========================================================
    elements.append(Paragraph("2. Tabel Iterasi Konvergensi", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    iter_data = [["Iterasi", "M", "P(b)", "Selisih"]]

    for row in data["iter_data"]:
        iter_data.append([
            str(row[0]),
            f"{row[1]:.6f}",
            f"{row[2]:.6f}",
            f"{row[3]:.6f}"
        ])

    table_iter = Table(iter_data)

    table_iter.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1d4ed8")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),

        # 👉 FIX: RATA KIRI (biar kayak laporan teknik beneran)
        ("ALIGN", (0,0), (-1,-1), "LEFT"),

        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 8),
    ]))

    elements.append(table_iter)
    elements.append(Spacer(1, 20))


    # =========================================================
    # GRAFIK (HD + CLEAN)
    # =========================================================
    elements.append(Paragraph("3. Grafik Probabilitas Blocking", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    img = io.BytesIO()
    fig.savefig(img, format="png", dpi=250, bbox_inches="tight")
    img.seek(0)

    elements.append(Image(img, width=500, height=280))
    elements.append(Spacer(1, 20))


    # =========================================================
    # KESIMPULAN (FORMAL INDONESIA)
    # =========================================================
    elements.append(Paragraph("4. Kesimpulan", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    kesimpulan = f"""
    Berdasarkan hasil simulasi menggunakan model Engset,
    sistem berada dalam kondisi <b>{data['status']}</b>.

    Nilai probabilitas blocking sebesar <b>{data['Pb']:.6f}</b>
    menunjukkan tingkat kepadatan trafik pada sistem.

    Hasil ini dapat digunakan untuk analisis kapasitas jaringan
    telekomunikasi secara lebih akurat.
    """

    elements.append(Paragraph(kesimpulan, styles["BodyText"]))

    doc.build(elements)
    buffer.seek(0)

    return buffer
