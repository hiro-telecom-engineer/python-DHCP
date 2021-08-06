from socket import socket, AF_INET, SOCK_DGRAM
import dhcp

# バッファサイズ指定
BUFSIZE = 1024
# ソケット
udp_serv_sock = ""
udp_serv_sock_broadcast = ""
c_addr = ""

def udp_init(values):
	global c_addr
	c_addr = values["c_addr"]

# 応答用ソケット
def udp_open(ip_addr):
	global udp_serv_sock
	# 受信側アドレスをtupleに格納
	src_addr = (ip_addr, 67)
	# ソケット作成
	udp_serv_sock = socket(AF_INET, SOCK_DGRAM)
	# 受信側アドレスでソケットを設定
	udp_serv_sock.bind(src_addr)
	print("サーバ起動:" + ip_addr)
	# While文を使用して常に受信待ちのループを実行
	while True:
		# ソケットにデータを受信した場合の処理
		# 受信データを変数に設定
		data, addr = udp_serv_sock.recvfrom(BUFSIZE)
		# 受信を出力
		# print(data, addr)
		# 受信データチェック
		result, res = dhcp.chk_data(data)
		if "error" !=  result:
			# 送信データを出力
			print(result + "送信")
			udp_serv_sock.sendto(res, (c_addr, 68))
