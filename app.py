# coding: utf -8
import PySimpleGUI as sg  # ライブラリの読み込み
import udp
import threading
import dhcp

# テーマの設定
sg.theme("SystemDefault ")

# ドメイン設定
L1 = [
	# DHCPサーバ設定
	[sg.Text("・サーバIPアドレス ", size=(20, 1)),
	 sg.InputText(default_text="192.168.0.1", text_color="#000000", background_color="#ffffff", size=(15, 1), key="s_addr")],
	# ドメイン設定3
	[sg.Text("・割り当てIPアドレス ", size=(20, 1)),
	 sg.InputText(default_text="192.168.0.100", text_color="#000000", background_color="#ffffff", size=(15, 1), key="c_addr")],
	[sg.Text("・リース期間 ", size=(20, 1)),
	 sg.InputText(default_text="3600", text_color="#000000", background_color="#ffffff", size=(15, 1), key="lease_time")],
	[sg.Text("・サブネットマスク ", size=(20, 1)),
	 sg.InputText(default_text="255.255.255.0", text_color="#000000", background_color="#ffffff", size=(15, 1), key="subnet_mask")],
	[sg.Button("DHCPサーバ起動", border_width=4, size=(15, 1), key="btn_dhcp_open")]]

# ウィンドウ作成
window = sg.Window("DHCP_SERVER ", L1)


def main():
	# イベントループ
	while True:
		# イベントの読み取り（イベント待ち）
		event, values = window.read()
		# 確認表示
		# print(" イベント:", event, ", 値:", values)
		# 終了条件（ None: クローズボタン）
		if event == "btn_dhcp_open":
			# DHCPサーバ初期値設定
			dhcp.init(values)
			udp.udp_init(values)
			# スレッド制御
			thread1 = threading.Thread(target=udp.udp_open, args=(values["s_addr"], ))
			thread1.setDaemon(True)
			thread1.start()
		elif event is None:
			break
	# 終了処理
	window.close()


if __name__ == '__main__':
	main()
