# colorful_info.py - Premium Info Website (WEB_MULTI.py Style)

from flask import Flask, render_template_string, request, jsonify
import requests
import json
import os
from datetime import datetime
import random

app = Flask(__name__)

# Configuration
API_BASE_URL = "https://stargamerff.qzz.io/accinfo?uid={uid}"
ICON_BASE_URL = "https://cdn.jsdelivr.net/gh/ShahGCreator/icon@main/PNG"

def format_timestamp(timestamp):
    try:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
    except:
        return str(timestamp)

def fetch_player_info(uid):
    try:
        url = f"{API_BASE_URL}?uid={uid}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def process_items(item_list):
    processed = []
    for item_id in item_list:
        icon_url = f"{ICON_BASE_URL}/{item_id}.png"
        processed.append({
            'id': item_id,
            'icon': icon_url
        })
    return processed

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌈 A4X ASH INFO · Player Database</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Rajdhani', sans-serif;
            min-height: 100vh;
            background: #0a0a0a;
            overflow-x: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        /* ===== BACKGROUND WITH COLORFUL EFFECTS ===== */
        .anime-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            overflow: hidden;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a0033 30%, #0a0015 60%, #1a0a00 100%);
        }

        .anime-bg::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 80%, rgba(255, 100, 0, 0.2) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255, 0, 100, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 50% 50%, rgba(255, 215, 0, 0.08) 0%, transparent 70%);
            z-index: 1;
        }

        /* ===== COLORFUL EMOJIS FLOATING ===== */
        .naruto-char {
            position: absolute;
            font-size: 120px;
            opacity: 0.1;
            z-index: 0;
            animation: floatChar 25s ease-in-out infinite;
            user-select: none;
            pointer-events: none;
            filter: drop-shadow(0 0 30px rgba(255, 165, 0, 0.2));
        }

        .naruto-char:nth-child(1) { top: 5%; left: 3%; animation-delay: 0s; font-size: 160px; color: #FF6B35; }
        .naruto-char:nth-child(2) { bottom: 10%; right: 3%; animation-delay: -6s; font-size: 140px; color: #FFD700; }
        .naruto-char:nth-child(3) { top: 50%; left: 50%; transform: translate(-50%, -50%); animation-delay: -12s; font-size: 220px; opacity: 0.06; color: #FF4500; }
        .naruto-char:nth-child(4) { top: 15%; right: 10%; animation-delay: -4s; font-size: 100px; color: #FF1493; }
        .naruto-char:nth-child(5) { bottom: 20%; left: 10%; animation-delay: -9s; font-size: 110px; color: #00BFFF; }
        .naruto-char:nth-child(6) { top: 40%; right: 5%; animation-delay: -15s; font-size: 80px; color: #7B68EE; }
        .naruto-char:nth-child(7) { bottom: 45%; left: 5%; animation-delay: -18s; font-size: 90px; color: #FF69B4; }
        .naruto-char:nth-child(8) { top: 20%; left: 50%; animation-delay: -3s; font-size: 70px; color: #FF6B35; }
        .naruto-char:nth-child(9) { bottom: 30%; right: 15%; animation-delay: -10s; font-size: 80px; color: #00ff64; }

        @keyframes floatChar {
            0%, 100% { transform: translateY(0px) rotate(0deg) scale(1); }
            25% { transform: translateY(-40px) rotate(5deg) scale(1.05); }
            75% { transform: translateY(40px) rotate(-5deg) scale(0.95); }
        }

        /* ===== PARTICLES ===== */
        .particles {
            position: absolute;
            width: 100%;
            height: 100%;
            z-index: 0;
        }

        .particle {
            position: absolute;
            border-radius: 50%;
            animation: particleFloat linear infinite;
            box-shadow: 0 0 15px currentColor;
        }

        @keyframes particleFloat {
            0% { transform: translateY(100vh) scale(0); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { transform: translateY(-10vh) scale(1); opacity: 0; }
        }

        /* ===== GLASS CARD ===== */
        .glass-card {
            position: relative;
            z-index: 1;
            width: 100%;
            max-width: 950px;
            background: rgba(10, 10, 30, 0.8);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 35px;
            padding: 45px;
            box-shadow: 
                0 40px 100px rgba(0, 0, 0, 0.9),
                0 0 80px rgba(255, 165, 0, 0.05),
                inset 0 1px 0 rgba(255, 255, 255, 0.05);
            animation: fadeInUp 0.8s ease-out;
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(60px) scale(0.98); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }

        /* ===== HEADER ===== */
        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .status-badge {
            display: inline-block;
            background: linear-gradient(135deg, rgba(0, 255, 100, 0.15), rgba(0, 255, 200, 0.05));
            border: 1px solid rgba(0, 255, 100, 0.25);
            padding: 8px 25px;
            border-radius: 50px;
            font-size: 13px;
            color: #00ff88;
            letter-spacing: 2px;
            margin-bottom: 15px;
            animation: pulse 2s ease-in-out infinite;
            font-weight: 600;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.6; transform: scale(0.98); }
        }

        .title {
            font-family: 'Orbitron', sans-serif;
            font-size: 48px;
            font-weight: 900;
            background: linear-gradient(135deg, #FF6B35, #FFD700, #FF1493, #00BFFF, #7B68EE, #FF6B35);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: rainbowGradient 4s ease-in-out infinite;
            text-shadow: none;
            letter-spacing: 2px;
        }

        @keyframes rainbowGradient {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }

        .subtitle {
            color: rgba(255, 255, 255, 0.4);
            font-size: 15px;
            margin-top: 10px;
            letter-spacing: 4px;
            font-weight: 400;
        }

        .subtitle i {
            color: #FFD700;
            margin: 0 8px;
            animation: glowPulse 1.5s ease-in-out infinite;
        }

        @keyframes glowPulse {
            0%, 100% { opacity: 0.5; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.2); }
        }

        /* ===== SOCIAL SECTION (WEB_MULTI.PY STYLE) ===== */
        .social-section {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
            margin-bottom: 30px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .social-card {
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 12px 24px;
            border-radius: 16px;
            text-decoration: none;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.06);
            min-width: 200px;
            justify-content: center;
        }

        .social-card:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
        }

        .social-card .icon-wrapper {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            flex-shrink: 0;
        }

        .social-card .info {
            display: flex;
            flex-direction: column;
        }

        .social-card .label {
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
            opacity: 0.5;
            font-weight: 600;
        }

        .social-card .username {
            font-size: 16px;
            font-weight: 700;
            color: #fff;
            font-family: 'Orbitron', sans-serif;
            letter-spacing: 0.5px;
        }

        .social-card.telegram {
            background: linear-gradient(135deg, rgba(0, 136, 204, 0.15), rgba(0, 136, 204, 0.05));
            border-color: rgba(0, 136, 204, 0.2);
        }

        .social-card.telegram:hover {
            background: linear-gradient(135deg, rgba(0, 136, 204, 0.25), rgba(0, 136, 204, 0.1));
            border-color: rgba(0, 136, 204, 0.4);
            box-shadow: 0 10px 40px rgba(0, 136, 204, 0.2);
        }

        .social-card.telegram .icon-wrapper {
            background: linear-gradient(135deg, #0088cc, #00aaff);
            color: #fff;
            box-shadow: 0 4px 15px rgba(0, 136, 204, 0.3);
        }

        .social-card.telegram .username {
            color: #00aaff;
        }

        .social-card.instagram {
            background: linear-gradient(135deg, rgba(225, 48, 108, 0.15), rgba(252, 175, 69, 0.05));
            border-color: rgba(225, 48, 108, 0.2);
        }

        .social-card.instagram:hover {
            background: linear-gradient(135deg, rgba(225, 48, 108, 0.25), rgba(252, 175, 69, 0.1));
            border-color: rgba(225, 48, 108, 0.4);
            box-shadow: 0 10px 40px rgba(225, 48, 108, 0.2);
        }

        .social-card.instagram .icon-wrapper {
            background: linear-gradient(135deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
            color: #fff;
            box-shadow: 0 4px 15px rgba(225, 48, 108, 0.3);
        }

        .social-card.instagram .username {
            color: #f09433;
        }

        /* ===== SEARCH SECTION ===== */
        .search-section {
            margin-bottom: 20px;
        }

        .search-box {
            display: flex;
            gap: 12px;
            background: rgba(255, 255, 255, 0.05);
            padding: 6px;
            border-radius: 60px;
            border: 1px solid rgba(255, 255, 255, 0.06);
            transition: all 0.4s ease;
        }

        .search-box:focus-within {
            border-color: rgba(255, 255, 255, 0.15);
            box-shadow: 0 0 40px rgba(255, 255, 255, 0.03);
        }

        .search-box input {
            flex: 1;
            padding: 16px 24px;
            background: transparent;
            border: none;
            color: #fff;
            font-size: 16px;
            font-family: 'Rajdhani', sans-serif;
            outline: none;
            font-weight: 600;
        }

        .search-box input::placeholder {
            color: rgba(255, 255, 255, 0.25);
        }

        .search-box button {
            padding: 16px 32px;
            background: linear-gradient(135deg, #FF6B35, #FFD700, #FF1493);
            border: none;
            border-radius: 50px;
            color: #fff;
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s ease;
            letter-spacing: 1px;
            white-space: nowrap;
        }

        .search-box button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 40px rgba(255, 107, 53, 0.3);
        }

        .search-box button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .search-box button i {
            margin-right: 8px;
        }

        /* ===== LOADING ===== */
        .loading-indicator {
            display: none;
            text-align: center;
            padding: 30px;
        }

        .loading-indicator.active {
            display: block;
        }

        .loader {
            display: inline-block;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            border: 4px solid rgba(255, 255, 255, 0.05);
            border-top-color: #FF6B35;
            border-right-color: #FFD700;
            border-bottom-color: #FF1493;
            border-left-color: #00BFFF;
            animation: spinLoader 1s linear infinite;
        }

        @keyframes spinLoader {
            to { transform: rotate(360deg); }
        }

        .loading-indicator p {
            color: rgba(255, 255, 255, 0.4);
            margin-top: 15px;
            font-family: 'Orbitron', monospace;
            font-size: 12px;
            letter-spacing: 2px;
        }

        /* ===== ERROR ===== */
        .error-box {
            display: none;
            text-align: center;
            padding: 30px;
            background: rgba(255, 107, 107, 0.05);
            border: 1px solid rgba(255, 107, 107, 0.15);
            border-radius: 16px;
            margin-top: 15px;
        }

        .error-box.active {
            display: block;
            animation: fadeInUp 0.4s ease;
        }

        .error-box .error-icon {
            font-size: 40px;
            margin-bottom: 10px;
        }

        .error-box p {
            color: rgba(255, 255, 255, 0.6);
            font-size: 16px;
        }

        /* ===== PROFILE CARD (Endpoint Style from WEB_MULTI.py) ===== */
        .profile-card {
            display: none;
            margin-top: 20px;
        }

        .profile-card.active {
            display: block;
            animation: fadeInUp 0.6s ease;
        }

        .endpoint {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 18px;
            padding: 20px 25px;
            margin-bottom: 16px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }

        .endpoint::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(180deg, #FF6B35, #FFD700, #FF1493, #00BFFF);
            border-radius: 4px;
        }

        .endpoint:hover {
            background: rgba(255, 255, 255, 0.06);
            border-color: rgba(255, 255, 255, 0.1);
            transform: translateX(8px);
            box-shadow: 0 5px 30px rgba(0, 0, 0, 0.3);
        }

        .endpoint-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 10px;
        }

        .endpoint-name {
            color: #fff;
            font-size: 17px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 12px;
            font-family: 'Orbitron', sans-serif;
        }

        .endpoint-name .badge {
            font-size: 10px;
            padding: 3px 14px;
            border-radius: 50px;
            letter-spacing: 1px;
            font-weight: 700;
        }

        .badge.profile {
            background: linear-gradient(135deg, rgba(255, 107, 53, 0.3), rgba(255, 215, 0, 0.1));
            color: #FF6B35;
            border: 1px solid rgba(255, 107, 53, 0.3);
        }

        .badge.stats {
            background: linear-gradient(135deg, rgba(0, 191, 255, 0.3), rgba(123, 104, 238, 0.1));
            color: #00BFFF;
            border: 1px solid rgba(0, 191, 255, 0.3);
        }

        .badge.skills {
            background: linear-gradient(135deg, rgba(255, 20, 147, 0.3), rgba(255, 105, 180, 0.1));
            color: #FF1493;
            border: 1px solid rgba(255, 20, 147, 0.3);
        }

        .endpoint-desc {
            color: rgba(255, 255, 255, 0.35);
            font-size: 12px;
            margin-top: 8px;
            letter-spacing: 1px;
        }

        .endpoint-desc i {
            margin-right: 8px;
        }

        .endpoint-desc .arrow {
            color: #FFD700;
        }

        /* ===== PROFILE HEADER ===== */
        .profile-header {
            display: flex;
            align-items: center;
            gap: 20px;
            flex-wrap: wrap;
        }

        .avatar {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            background: linear-gradient(135deg, #FF6B35, #FFD700, #FF1493, #00BFFF);
            background-size: 300% 300%;
            animation: rainbowGradient 4s ease-in-out infinite;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            color: #fff;
            flex-shrink: 0;
            box-shadow: 0 0 30px rgba(255, 107, 53, 0.2);
        }

        .profile-info {
            flex: 1;
        }

        .profile-info .name {
            font-family: 'Orbitron', sans-serif;
            font-size: 22px;
            color: #fff;
            font-weight: 700;
        }

        .profile-info .bio {
            color: rgba(255, 255, 255, 0.4);
            font-size: 13px;
            margin-top: 2px;
        }

        .profile-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 6px;
        }

        .profile-tag {
            padding: 3px 14px;
            border-radius: 20px;
            font-size: 10px;
            font-weight: 600;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.06);
            color: rgba(255, 255, 255, 0.6);
            font-family: 'Orbitron', monospace;
            letter-spacing: 0.5px;
        }

        .profile-tag.highlight {
            background: linear-gradient(135deg, #FF6B35, #FFD700);
            border-color: transparent;
            color: #fff;
        }

        .profile-tag.green { background: rgba(0, 255, 100, 0.15); border-color: #00ff64; color: #00ff64; }
        .profile-tag.blue { background: rgba(0, 191, 255, 0.15); border-color: #00BFFF; color: #00BFFF; }
        .profile-tag.purple { background: rgba(123, 104, 238, 0.15); border-color: #7B68EE; color: #7B68EE; }
        .profile-tag.pink { background: rgba(255, 20, 147, 0.15); border-color: #FF1493; color: #FF1493; }

        /* ===== STATS GRID ===== */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 12px;
            padding: 12px;
            text-align: center;
            transition: all 0.3s ease;
        }

        .stat-card:hover {
            transform: translateY(-3px);
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(255, 255, 255, 0.08);
        }

        .stat-card .stat-icon {
            font-size: 20px;
            display: block;
            margin-bottom: 2px;
        }

        .stat-card .stat-value {
            font-family: 'Orbitron', monospace;
            font-size: 18px;
            font-weight: 700;
            color: #fff;
        }

        .stat-card .stat-label {
            color: rgba(255, 255, 255, 0.25);
            font-size: 9px;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-family: 'Orbitron', monospace;
        }

        /* ===== ITEMS GRID ===== */
        .items-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
            gap: 10px;
            margin-top: 10px;
        }

        .item-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 10px;
            padding: 8px;
            text-align: center;
            transition: all 0.3s ease;
        }

        .item-card:hover {
            transform: scale(1.05);
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(255, 255, 255, 0.1);
        }

        .item-card img {
            width: 35px;
            height: 35px;
            border-radius: 6px;
        }

        .item-card .item-id {
            color: rgba(255, 255, 255, 0.15);
            font-size: 8px;
            margin-top: 3px;
            font-family: 'Orbitron', monospace;
        }

        /* ===== CLAN & SOCIAL ===== */
        .clan-social {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 15px;
        }

        @media (max-width: 600px) {
            .clan-social {
                grid-template-columns: 1fr;
            }
        }

        .info-box {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 12px;
            padding: 15px;
        }

        .info-box .box-title {
            font-family: 'Orbitron', monospace;
            font-size: 11px;
            color: rgba(255, 255, 255, 0.3);
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .info-box .box-content {
            color: rgba(255, 255, 255, 0.6);
            line-height: 1.6;
            font-size: 13px;
        }

        .info-box .box-content .highlight {
            color: #fff;
            font-weight: 600;
        }

        /* ===== FOOTER ===== */
        .footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            color: rgba(255, 255, 255, 0.15);
            font-size: 12px;
            letter-spacing: 2px;
        }

        .footer .heart {
            color: #FF1493;
            animation: heartBeat 1.5s ease-in-out infinite;
            display: inline-block;
        }

        @keyframes heartBeat {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.3); }
        }

        .footer a {
            color: #FFD700;
            text-decoration: none;
            transition: color 0.3s;
            font-weight: 600;
        }

        .footer a:hover {
            color: #FF6B35;
        }

        /* ===== TOAST ===== */
        .toast {
            position: fixed;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: rgba(0, 0, 0, 0.95);
            color: #fff;
            padding: 15px 35px;
            border-radius: 16px;
            border: 1px solid rgba(255, 215, 0, 0.2);
            font-size: 14px;
            z-index: 999;
            opacity: 0;
            transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            backdrop-filter: blur(15px);
            font-family: 'Rajdhani', sans-serif;
            font-weight: 600;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
        }

        .toast.show {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }

        .toast .toast-icon {
            margin-right: 12px;
        }

        /* ===== RESPONSIVE ===== */
        @media (max-width: 768px) {
            .glass-card {
                padding: 25px 18px;
                border-radius: 25px;
            }

            .title {
                font-size: 30px;
            }

            .social-section {
                gap: 12px;
                padding: 12px;
            }

            .social-card {
                padding: 10px 16px;
                min-width: 140px;
                flex: 1;
            }

            .search-box {
                flex-direction: column;
                border-radius: 20px;
                padding: 12px;
            }

            .search-box input {
                text-align: center;
                padding: 12px 16px;
                font-size: 14px;
            }

            .search-box button {
                width: 100%;
                justify-content: center;
                padding: 14px;
            }

            .profile-header {
                flex-direction: column;
                text-align: center;
            }

            .profile-tags {
                justify-content: center;
            }

            .stats-grid {
                grid-template-columns: 1fr 1fr;
            }

            .items-grid {
                grid-template-columns: repeat(auto-fill, minmax(50px, 1fr));
            }

            .naruto-char {
                font-size: 70px !important;
            }

            .subtitle {
                font-size: 12px;
                letter-spacing: 2px;
            }
        }

        @media (max-width: 480px) {
            .title {
                font-size: 22px;
            }

            .glass-card {
                padding: 16px 12px;
                border-radius: 20px;
            }

            .status-badge {
                font-size: 11px;
                padding: 6px 18px;
            }

            .social-card {
                padding: 8px 12px;
                min-width: 100px;
            }

            .social-card .username {
                font-size: 11px;
            }

            .social-card .label {
                font-size: 8px;
            }

            .social-card .icon-wrapper {
                width: 32px;
                height: 32px;
                font-size: 15px;
            }
        }
/* SHARE PROFILE BUTTON */
.share-btn {
    width: 100%;
    margin-top: 12px;
    padding: 13px 18px;
    border: 1px solid rgba(0, 191, 255, 0.5);
    border-radius: 12px;
    background: linear-gradient(135deg, #00BFFF, #7B68EE);
    color: white;
    font-size: 14px;
    font-weight: 800;
    cursor: pointer;
    box-shadow: 0 0 15px rgba(0, 191, 255, 0.35);
    transition: 0.25s ease;
}

.share-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 25px rgba(123, 104, 238, 0.65);
}

.share-btn:active {
    transform: scale(0.97);
}        
    </style>
</head>
<body>

    <!-- ===== BACKGROUND ===== -->
    <div class="anime-bg">
        <div class="naruto-char">🍥</div>
        <div class="naruto-char">⚔️</div>
        <div class="naruto-char">🌀</div>
        <div class="naruto-char">🔥</div>
        <div class="naruto-char">💥</div>
        <div class="naruto-char">⭐</div>
        <div class="naruto-char">⚡</div>
        <div class="naruto-char">🌈</div>
        <div class="naruto-char">🎯</div>
        <div class="particles" id="particles"></div>
    </div>

    <!-- ===== TOAST ===== -->
    <div class="toast" id="toast">
        <span class="toast-icon">✅</span>
        <span id="toastMessage">Success!</span>
    </div>

    <!-- ===== GLASS CARD ===== -->
    <div class="glass-card">

        <!-- Header -->
        <div class="header">
            <div class="status-badge">
                <i class="fas fa-circle" style="color: #00ff64; font-size: 8px; margin-right: 8px;"></i>
                ONLINE ✅
            </div>
            <h1 class="title">🌈 A4X ASH INFO</h1>
            <p class="subtitle">
                <i class="fas fa-star"></i> PLAYER DATABASE <i class="fas fa-star"></i>
            </p>
        </div>

        <!-- Social Section (WEB_MULTI.py Style) -->
        <div class="social-section">
            <a href="https://t.me/a4x_ash" target="_blank" class="social-card telegram">
                <div class="icon-wrapper">
                    <i class="fab fa-telegram-plane"></i>
                </div>
                <div class="info">
                    <span class="label">Telegram ID</span>
                    <span class="username">💫 TG DM</span>
                </div>
            </a>
            <a href="https://t.me/a4x_x_ff" target="_blank" class="social-card telegram">
                <div class="icon-wrapper">
                    <i class="fab fa-telegram-plane"></i>
                </div>
                <div class="info">
                    <span class="label">Telegram Channel</span>
                    <span class="username">TG CHHANAL 🐉</span>
                </div>
            </a>
            <a href="https://instagram.com/official_ash_x1" target="_blank" class="social-card instagram">
                <div class="icon-wrapper">
                    <i class="fab fa-instagram"></i>
                </div>
                <div class="info">
                    <span class="label">Instagram</span>
                    <span class="username">official_ash_x1</span>
                </div>
            </a>
        </div>

        <!-- Search -->
        <div class="search-section">
            <div class="search-box">
                <input type="text" id="uidInput" placeholder="🔍 Enter Player UID..." />
                <button id="searchBtn">
                    <i class="fas fa-rocket"></i> SEARCH
                </button>
            </div>
        </div>

        <!-- Loading -->
        <div class="loading-indicator" id="loadingIndicator">
            <div class="loader"></div>
            <p>🌟 FETCHING PLAYER DATA...</p>
        </div>

        <!-- Error -->
        <div class="error-box" id="errorBox">
            <div class="error-icon">😅</div>
            <p>Oops! Player not found. Please check the UID.</p>
        </div>

        <!-- ===== PROFILE (Endpoint Style from WEB_MULTI.py) ===== -->
        <div class="profile-card" id="profileCard">

            <!-- Profile Endpoint -->
            <div class="endpoint">
                <div class="endpoint-header">
                    <div class="endpoint-name">
                        👤 PLAYER PROFILE
                        <span class="badge profile">INFO</span>
                    </div>
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span id="playerStatus" style="color:#00ff64; font-size:12px;">● ONLINE</span>
                    </div>
                </div>
                <div class="endpoint-desc">
                    <i class="fas fa-arrow-right arrow"></i> Player Details
                </div>

                <!-- Profile Content -->
                <div style="margin-top:15px;">
                    <div class="profile-header">
                        <div class="avatar" id="avatarEmoji">👤</div>
                        <div class="profile-info">
                            <div class="name" id="playerName">Player Name</div>
                            <div class="bio" id="playerBio">ID: Loading...</div>
                            <div class="profile-tags" id="playerTags"></div>
                        </div>
                    </div>
                </div>
            </div>
            
                        <button id="shareBtn" class="share-btn">
                📤 SHARE PROFILE
            </button>

            <!-- Stats Endpoint -->
            <div class="endpoint">
                <div class="endpoint-header">
                    <div class="endpoint-name">
                        📊 PLAYER STATS
                        <span class="badge stats">STATS</span>
                    </div>
                </div>
                <div class="endpoint-desc">
                    <i class="fas fa-arrow-right arrow"></i> Level · Rank · Experience
                </div>
                <div class="stats-grid" id="statsGrid">
                    <div class="stat-card">
                        <span class="stat-icon">⭐</span>
                        <div class="stat-value" id="statLevel">0</div>
                        <div class="stat-label">Level</div>
                    </div>
                    <div class="stat-card">
                        <span class="stat-icon">🏆</span>
                        <div class="stat-value" id="statRank">0</div>
                        <div class="stat-label">Rank</div>
                    </div>
                    <div class="stat-card">
                        <span class="stat-icon">💎</span>
                        <div class="stat-value" id="statMaxRank">0</div>
                        <div class="stat-label">Max Rank</div>
                    </div>
                    <div class="stat-card">
                        <span class="stat-icon">📊</span>
                        <div class="stat-value" id="statExp">0</div>
                        <div class="stat-label">Experience</div>
                    </div>
                    <div class="stat-card">
                        <span class="stat-icon">❤️</span>
                        <div class="stat-value" id="statLikes">0</div>
                        <div class="stat-label">Likes</div>
                    </div>
                    <div class="stat-card">
                        <span class="stat-icon">🎖️</span>
                        <div class="stat-value" id="statBadges">0</div>
                        <div class="stat-label">Badges</div>
                    </div>
                </div>
            </div>

            <!-- Skills Endpoint -->
            <div class="endpoint" id="skillsSection">
                <div class="endpoint-header">
                    <div class="endpoint-name">
                        🎯 EQUIPPED SKILLS
                        <span class="badge skills">SKILLS</span>
                    </div>
                </div>
                <div class="endpoint-desc">
                    <i class="fas fa-arrow-right arrow"></i> Active Skills
                </div>
                <div class="items-grid" id="skillsGrid"></div>
            </div>

            <!-- Weapons Endpoint -->
            <div class="endpoint" id="weaponsSection">
                <div class="endpoint-header">
                    <div class="endpoint-name">
                        🔫 WEAPON SKINS
                        <span class="badge stats">WEAPONS</span>
                    </div>
                </div>
                <div class="endpoint-desc">
                    <i class="fas fa-arrow-right arrow"></i> Owned Weapon Skins
                </div>
                <div class="items-grid" id="weaponsGrid"></div>
            </div>

            <!-- Clan & Social -->
            <div class="clan-social">
                <div class="endpoint" style="margin-bottom:0;">
                    <div class="endpoint-header">
                        <div class="endpoint-name" style="font-size:14px;">
                            ⚔️ CLAN
                            <span class="badge profile">CLAN</span>
                        </div>
                    </div>
                    <div class="box-content" id="clanInfo" style="color:rgba(255,255,255,0.6); font-size:13px;">No clan affiliation</div>
                </div>
                <div class="endpoint" style="margin-bottom:0;">
                    <div class="endpoint-header">
                        <div class="endpoint-name" style="font-size:14px;">
                            💬 BIO / SOCIAL
                            <span class="badge stats">SOCIAL</span>
                        </div>
                    </div>
                    <div class="box-content" id="socialInfo" style="color:rgba(255,255,255,0.6); font-size:13px;">No bio available</div>
                </div>
            </div>

        </div>

        <!-- Footer (WEB_MULTI.py Style) -->
        <div class="footer">
            Powered by <a href="https://t.me/a4x_ash" target="_blank">@a4x_ash</a> 
            <span class="heart">❤️</span>
            <a href="https://t.me/a4x_x_ff" target="_blank">A4X LIKE GROUP</a>
        </div>

    </div>

    <script>
        // ============================
        // PARTICLES
        // ============================
        const colors = ['#FF6B35', '#FFD700', '#FF1493', '#00BFFF', '#7B68EE', '#FF4500', '#00ff64', '#FF69B4'];
        const container = document.getElementById('particles');
        for (let i = 0; i < 50; i++) {
            const p = document.createElement('div');
            p.className = 'particle';
            const size = Math.random() * 5 + 2;
            p.style.width = size + 'px';
            p.style.height = size + 'px';
            p.style.left = Math.random() * 100 + '%';
            const color = colors[Math.floor(Math.random() * colors.length)];
            p.style.background = color;
            p.style.color = color;
            p.style.animationDuration = (Math.random() * 20 + 10) + 's';
            p.style.animationDelay = (Math.random() * 20) + 's';
            p.style.opacity = Math.random() * 0.4 + 0.1;
            container.appendChild(p);
        }

        // ============================
        // TOAST
        // ============================
        function showToast(message, type = 'info') {
            const toast = document.getElementById('toast');
            const toastMsg = document.getElementById('toastMessage');
            toastMsg.textContent = message;
            toast.classList.add('show');
            clearTimeout(toast._timeout);
            toast._timeout = setTimeout(() => {
                toast.classList.remove('show');
            }, 3000);
        }

        // ============================
        // FETCH PLAYER
        // ============================
        const searchBtn = document.getElementById('searchBtn');
        const uidInput = document.getElementById('uidInput');
        const loadingIndicator = document.getElementById('loadingIndicator');
        const errorBox = document.getElementById('errorBox');
        const profileCard = document.getElementById('profileCard');

        async function fetchPlayer(uid) {
            if (!uid || uid.trim() === '') {
                showToast('⚠️ Please enter a valid UID', 'warning');
                return;
            }

            loadingIndicator.classList.add('active');
            profileCard.classList.remove('active');
            errorBox.classList.remove('active');
            searchBtn.disabled = true;
            searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> LOADING...';

            try {
                const response = await fetch(`/api/player/${uid.trim()}`);
                if (!response.ok) throw new Error('Player not found');
                const data = await response.json();
                renderProfile(data);
                profileCard.classList.add('active');
                showToast('✨ Player found! Welcome! 🎉', 'success');
            } catch (error) {
                errorBox.classList.add('active');
                showToast('❌ Player not found!', 'error');
            } finally {
                loadingIndicator.classList.remove('active');
                searchBtn.disabled = false;
                searchBtn.innerHTML = '<i class="fas fa-rocket"></i> SEARCH';
            }
        }

        function renderProfile(data) {
            if (data.basic) {
                const basic = data.basic;
                document.getElementById('playerName').textContent = basic.nickname || 'Unknown';
                document.getElementById('playerBio').textContent = `ID: ${basic.account_id || 'N/A'} · ${basic.region || 'N/A'}`;
                
                const tags = document.getElementById('playerTags');
                tags.innerHTML = `
                    <span class="profile-tag highlight">⭐ LVL ${basic.level || 0}</span>
                    <span class="profile-tag green">🏆 RANK ${basic.rank || 0}</span>
                    <span class="profile-tag blue">🌍 ${basic.region || 'N/A'}</span>
                    <span class="profile-tag pink">❤️ ${basic.liked || 0}</span>
                    <span class="profile-tag purple">🎖️ ${basic.badge_cnt || 0}</span>
                `;

                document.getElementById('statLevel').textContent = basic.level || 0;
                document.getElementById('statRank').textContent = basic.rank || 0;
                document.getElementById('statMaxRank').textContent = basic.max_rank || 0;
                document.getElementById('statExp').textContent = (basic.exp || 0).toLocaleString();
                document.getElementById('statLikes').textContent = basic.liked || 0;
                document.getElementById('statBadges').textContent = basic.badge_cnt || 0;

                document.getElementById('avatarEmoji').textContent = 
                    basic.nickname ? basic.nickname.charAt(0).toUpperCase() : '👤';
            }

            // Skills
            if (data.skills && data.skills.length > 0) {
                const grid = document.getElementById('skillsGrid');
                grid.innerHTML = data.skills.map(skill => `
                    <div class="item-card">
                        <img src="${skill.icon}" alt="Skill" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2235%22 height=%2235%22%3E%3Crect width=%2235%22 height=%2235%22 fill=%22%231a1a2e%22/%3E%3Ctext x=%2217.5%22 y=%2222%22 text-anchor=%22middle%22 fill=%22%23ffffff%22 font-size=%2210%22 font-family=%22monospace%22%3E${skill.id}%3C/text%3E%3C/svg%3E'">
                        <div class="item-id">${skill.id}</div>
                    </div>
                `).join('');
                document.getElementById('skillsSection').style.display = 'block';
            } else {
                document.getElementById('skillsSection').style.display = 'none';
            }

            // Weapons
            if (data.basic && data.basic.weapons && data.basic.weapons.length > 0) {
                const grid = document.getElementById('weaponsGrid');
                grid.innerHTML = data.basic.weapons.map(weapon => `
                    <div class="item-card">
                        <img src="${weapon.icon}" alt="Weapon" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2235%22 height=%2235%22%3E%3Crect width=%2235%22 height=%2235%22 fill=%22%231a1a2e%22/%3E%3Ctext x=%2217.5%22 y=%2222%22 text-anchor=%22middle%22 fill=%22%23ffffff%22 font-size=%2210%22 font-family=%22monospace%22%3E${weapon.id}%3C/text%3E%3C/svg%3E'">
                        <div class="item-id">${weapon.id}</div>
                    </div>
                `).join('');
                document.getElementById('weaponsSection').style.display = 'block';
            } else {
                document.getElementById('weaponsSection').style.display = 'none';
            }

            // Clan
            if (data.clan) {
                const clan = data.clan;
                document.getElementById('clanInfo').innerHTML = `
                    <span class="highlight">${clan.name || 'No Clan'}</span><br>
                    Level ${clan.level || 0} · ${clan.members || 0}/${clan.max_members || 0} members
                `;
            } else {
                document.getElementById('clanInfo').textContent = 'No clan affiliation';
            }

            // Social
            if (data.social) {
                const social = data.social;
                document.getElementById('socialInfo').innerHTML = `
                    ${social.highlight ? social.highlight : 'No bio available'}<br>
                    <span style="font-size:10px;color:rgba(255,255,255,0.2);">
                        ${social.gender || 'Unknown'} · ${social.privacy || 'Private'}
                    </span>
                `;
            } else {
                document.getElementById('socialInfo').textContent = 'No bio available';
            }
        }

        // ============================
        // EVENT LISTENERS
        // ============================
        searchBtn.addEventListener('click', () => fetchPlayer(uidInput.value));
        uidInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') fetchPlayer(uidInput.value);
        });

        // Auto-fetch from URL
        const urlParams = new URLSearchParams(window.location.search);
        const uidParam = urlParams.get('uid');
        if (uidParam) {
            uidInput.value = uidParam;
            setTimeout(() => fetchPlayer(uidParam), 1000);
        }

        // Welcome toast
        setTimeout(() => {
            showToast('🌈 Welcome to A4X ASH INFO! Enter a UID to start.', 'success');
        }, 1500);

        console.log('🌈 A4X ASH INFO · Premium Player Database');
        console.log('✨ Made with ❤️ by A4X ASH');
        
// ============================
// SHARE PROFILE
// ============================
const shareBtn = document.getElementById('shareBtn');

if (shareBtn) {
    shareBtn.addEventListener('click', async () => {
        const uid = uidInput.value.trim();

        if (!uid) {
            showToast('⚠️ First enter a UID!', 'warning');
            return;
        }

        const shareUrl = `${window.location.origin}/?uid=${encodeURIComponent(uid)}`;

        try {
            if (navigator.share) {
                await navigator.share({
                    title: 'A4X ASH Player Profile',
                    text: `🎮 Free Fire Player UID: ${uid}`,
                    url: shareUrl
                });
            } else {
                await navigator.clipboard.writeText(shareUrl);
                showToast('🔗 Profile link copied!', 'success');
            }
        } catch (error) {
            console.log('Share cancelled');
        }
    });
}    
    
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/player/<uid>')
def get_player(uid):
    data = fetch_player_info(uid)
    if not data:
        return jsonify({'error': 'Player not found'}), 404
    
    formatted_data = {}
    
    if 'basic_info' in data:
        basic = data['basic_info']
        formatted_data['basic'] = {
            'nickname': basic.get('nickname', 'Unknown'),
            'level': basic.get('level', 0),
            'exp': basic.get('exp', 0),
            'rank': basic.get('rank', 0),
            'max_rank': basic.get('max_rank', 0),
            'ranking_points': basic.get('ranking_points', 0),
            'liked': basic.get('liked', 0),
            'region': basic.get('region', 'N/A'),
            'account_id': basic.get('account_id', 0),
            'badge_cnt': basic.get('badge_cnt', 0),
            'weapons': process_items(basic.get('weapon_skin_shows', []))
        }
    
    if 'profile_info' in data:
        profile = data['profile_info']
        if 'equipped_skills' in profile:
            formatted_data['skills'] = process_items(profile['equipped_skills'])
    
    if 'clan_basic_info' in data:
        clan = data['clan_basic_info']
        formatted_data['clan'] = {
            'name': clan.get('clan_name', 'No Clan'),
            'level': clan.get('clan_level', 0),
            'members': clan.get('current_members', 0),
            'max_members': clan.get('max_members', 0)
        }
    
    if 'social_info' in data:
        social = data['social_info']
        formatted_data['social'] = {
            'highlight': social.get('social_highlight', ''),
            'gender': social.get('gender', 'Unknown'),
            'privacy': social.get('privacy', 'Private')
        }
    
    return jsonify(formatted_data)

app.debug = False

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 9999))
    app.run(host='0.0.0.0', port=port, debug=False)