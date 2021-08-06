import dhcp_env

# グローバル変数
s_addr = ""
c_addr = ""
lease_time = ""
subnet_mask = ""
xid = ""

# 初期値設定関数
def init(values):
    global s_addr
    global c_addr
    global lease_time
    global subnet_mask
    s_addr = values["s_addr"].split(".")
    c_addr = values["c_addr"].split(".")
    lease_time = int(values["lease_time"])
    subnet_mask =  values["subnet_mask"].split(".")


def chk_data(data):
    global s_addr
    global c_addr
    chk_cookie = ""
    chk_dhcp_msg_type = ""
    result = "error"
    res = ""
    # データ長確認
    if dhcp_env.POS_MGIC_COOKIE + 3 < len(data):
        # Magic cookie確認
        chk_cookie += str(data[dhcp_env.POS_MGIC_COOKIE:dhcp_env.POS_MGIC_COOKIE + dhcp_env.LEN_MGIC_COOKIE].hex())
        if dhcp_env.MGIC_COOKIE == chk_cookie:
            # メッセージタイプ確認
            chk_dhcp_msg_type += str(data[dhcp_env.POS_DHCP_MASAGE_TYPE:dhcp_env.POS_DHCP_MASAGE_TYPE + dhcp_env.LEN_DHCP_MASAGE_TYPE].hex())
            if dhcp_env.OP_DHCP_MASAGE_TYPE_DISCOVER == chk_dhcp_msg_type:
                print("DHCP DISCOVER受信")
                # DHCP OFFER応答
                result = "DHCP OFFER"
                res = mk_data(data)
            elif dhcp_env.OP_DHCP_MASAGE_TYPE_REQUEST == chk_dhcp_msg_type:
                print("DHCP REQUEST受信")
                # DHCP ACK応答
                result = "DHCP ACK"
                res = mk_data(data)
    return result, res


def mk_data(data):
    global s_addr
    global c_addr
    global lease_time
    global subnet_mask
    res = dhcp_env.MTYPE_REPLY + dhcp_env.HTYPE_ETHER + dhcp_env.HLEN_MAC + dhcp_env.HOPS
    # xid取得、設定
    xid = str(data[dhcp_env.POS_XID:dhcp_env.POS_XID + dhcp_env.LEN_XID].hex())
    res += xid
    # SECS、FLAGS設定
    res += dhcp_env.SECS + dhcp_env.FLAGS
    # アドレス設定
    res += dhcp_env.CIADDR
    for i in range(len(c_addr)):
        res += format(int(c_addr[i]), '02x')
    for i in range(len(s_addr)):
        res += format(int(s_addr[i]), '02x')
    res += dhcp_env.GIADDR
    # chaddr取得、設定
    chaddr = str(data[dhcp_env.POS_CHADDR:dhcp_env.POS_CHADDR + dhcp_env.LEN_CHADDR].hex())
    res += chaddr
    # SAME,FILE設定
    res += dhcp_env.SAME
    res += dhcp_env.FILE
    # Magic Cookie
    res += dhcp_env.MGIC_COOKIE
    # OP(メッセージタイプ)
    recv_type = str(data[dhcp_env.POS_OP_DHCP_MASAGE_TYPE:dhcp_env.POS_OP_DHCP_MASAGE_TYPE + dhcp_env.LEN_OP_DHCP_MASAGE_TYPE].hex())
    # 受信メッセージタイプがDICOVER
    if dhcp_env.OP_DHCP_MASAGE_TYPE_DISCOVER == recv_type:
        res += dhcp_env.OP_DHCP_MASAGE_TYPE_OFFER
    # 受信メッセージタイプがREQUEST
    elif dhcp_env.OP_DHCP_MASAGE_TYPE_REQUEST == recv_type:
        res += dhcp_env.OP_DHCP_MASAGE_TYPE_ACK
    # リース時間設定
    res += dhcp_env.OP_IP_LEASE_TIME + format(lease_time, '08x')
    # サブネットマスク
    res += dhcp_env.OP_IP_SUBNET_MASK
    for i in range(len(subnet_mask)):
        res += format(int(subnet_mask[i]), '02x')
    # OP最終位置
    res += "FF"
    # byte型へ変換
    res = bytes.fromhex(res)

    return res
