# Modern Sidebar Layout - Cyan Theme

MAIN_STYLESHEET = """
#rootFrame {
    background-color: #FFFFFF;
    border-radius: 12px;
    border: 1px solid #E5E7EB;
}

#sidebar {
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, 
                                      stop:0 #ECFEFF, 
                                      stop:0.5 #F0FDFA, 
                                      stop:1 #FFFFFF);
    border-top-left-radius: 12px;
    border-bottom-left-radius: 12px;
    border-right: 1px solid #E2E8F0;
}

#contentArea {
    background-color: #FFFFFF;
    border-top-right-radius: 12px;
    border-bottom-right-radius: 12px;
}

#appName {
    color: #0F172A;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.02em;
    font-family: 'Segoe UI', sans-serif;
}
#appDesc {
    color: #94A3B8;
    font-size: 11px;
    font-weight: 500;
    font-family: 'Segoe UI', sans-serif;
}

#contentHeader {
    border-bottom: 1px solid #F1F5F9;
}
#headerTitle {
    color: #0F172A;
    font-size: 14px;
    font-weight: 600;
    font-family: 'Segoe UI', sans-serif;
}

#minBtn, #closeBtn {
    background: transparent;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    color: #94A3B8;
    padding: 0;
}
#minBtn:hover {
    background: #F1F5F9;
    color: #0F172A;
}
#closeBtn:hover {
    background: #FEF2F2;
    color: #EF4444;
}

#tableWidget {
    border: none;
    background-color: transparent;
    gridline-color: transparent;
    font-family: 'Segoe UI', sans-serif;
    font-size: 12px;
    selection-background-color: #ECFEFF;
}
#tableWidget::item {
    padding: 14px 16px;
    border-bottom: 1px solid #F1F5F9;
    color: #334155;
}
#tableWidget::item:hover {
    background-color: #F8FAFC;
}
#tableWidget::item:selected {
    background-color: #ECFEFF;
    color: #0F172A;
}
#tableWidget QHeaderView::section {
    background-color: transparent;
    color: #94A3B8;
    font-size: 10px;
    font-weight: 700;
    font-family: 'Segoe UI', sans-serif;
    padding: 12px 16px;
    border: none;
    border-bottom: 1px solid #E2E8F0;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
#tableWidget QTableCornerButton::section {
    background-color: transparent;
    border: none;
}

#emptyLabel {
    color: #94A3B8;
    font-size: 12px;
    font-family: 'Segoe UI', sans-serif;
}

#statusCard {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
}
#statusText {
    font-size: 11px;
    color: #64748B;
    font-family: 'Segoe UI', sans-serif;
    font-weight: 600;
}
"""