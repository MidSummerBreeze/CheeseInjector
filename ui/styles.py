# Modern Sidebar Layout - Cyan Theme with Acrylic Support

MAIN_STYLESHEET = """
#rootFrame {
    background-color: rgba(255, 255, 255, 200);
    border-radius: 12px;
}

#sidebar {
    background-color: rgba(236, 254, 255, 130);
    border-top-left-radius: 12px;
    border-bottom-left-radius: 12px;
    border-right: 1px solid rgba(255, 255, 255, 100);
}

#contentArea {
    background-color: transparent;
    border-top-right-radius: 12px;
    border-bottom-right-radius: 12px;
}

#appName {
    color: #0F172A;
    font-size: 20px;
    font-weight: 550;
    letter-spacing: -0.02em;
    font-family: 'Segoe UI', sans-serif;
}
#appDesc {
    color: #0E7490;
    font-size: 11px;
    font-weight: 500;
    font-family: 'Segoe UI', sans-serif;
}

#contentHeader {
    background-color: rgba(255, 255, 255, 50);
    border-bottom: 1px solid rgba(255, 255, 255, 150);
}
#headerTitle {
    color: #0F172A;
    font-size: 14px;
    font-weight: 500;
    font-family: 'Segoe UI', sans-serif;
}

#minBtn, #closeBtn {
    background: rgba(255, 255, 255, 100);
    border: none;
    border-radius: 6px;
    font-size: 13px;
    color: #475569;
    padding: 0;
}
#minBtn:hover {
    background: rgba(241, 245, 249, 220);
    color: #0F172A;
}
#closeBtn:hover {
    background: rgba(239, 68, 68, 180);
    color: #FFFFFF;
}

#tableWidget {
    border: none;
    background-color: transparent;
    gridline-color: transparent;
    font-family: 'Segoe UI', sans-serif;
    font-size: 12px;
    outline: none;
}
#tableWidget::item {
    padding: 14px 16px;
    border-bottom: 1px solid rgba(226, 232, 240, 150);
    color: #334155;
}
#tableWidget::item:selected {
    background-color: #CFFAFE;
    color: #0E7490;
    font-weight: 600;
}

/* Force header background transparent and text centered */
#tableWidget QHeaderView {
    background-color: transparent;
    border: none;
}
#tableWidget QHeaderView::section {
    background-color: transparent;
    color: #64748B;
    font-size: 11px;
    font-weight: 600;
    font-family: 'Segoe UI', sans-serif;
    padding: 12px 16px;
    border: none;
    border-bottom: 1px solid rgba(255, 255, 255, 150);
    text-align: center;
}
#tableWidget QTableCornerButton::section {
    background-color: transparent;
    border: none;
}

#emptyLabel {
    color: #64748B;
    font-size: 12px;
    font-family: 'Segoe UI', sans-serif;
}

/* Toast Styles */
#toast {
    background-color: #FFFFFF;
    border-radius: 8px;
    border: 1px solid #E2E8F0;
}
#toastTitle {
    font-size: 13px;
    font-weight: 600;
    font-family: 'Segoe UI', sans-serif;
}
#toastMessage {
    color: #334155;
    font-size: 12px;
    font-family: 'Segoe UI', sans-serif;
}
"""