import MySQLdb

conn = MySQLdb.connect(host='10.28.218.81', user='veveo', passwd="veveo123", db='YOUTUBECLIPSDB', charset='utf8')
cur = conn.cursor()


'''
channel_dict1 = {"WIKI37259045":"UC-lHJZR3Gqxm24_Vd_AJ5Yw", "WIKI12346158":"UCY30JRSgfhYXA6i6xX1erWg", "WIKI41312749":"UCVtFOytbRpEvzLjvqGG5gxQ", "WIKI36336637":"UC0v-tlzsn0QZwJnkiaUSJVQ", "OVP100018":"UCzwzVFgZa3AS9IPLPfJjf1w", "WIKI43386202":"UCnOVVuoLJ_1YY8A0V802wHA", "WIKI49751876":"UCaa-Kp29T1Ub29NPl5mnghQ", "OVP100002":"UC30ar4xgM8qm78A5SNbneSg", "OVP100003":"UCtUF5knabzU3gf6pJ_EdTEw", "WIKI523032":"UCRY5dYsbIN5TylSbd7gVnZg", "WIKI7925760":"UCYYondpOMfeyI-Zmoe2Ckfw", "WGER3690462":"UCF_sh7efmoosuGZVYWzryiQ", "RV1467511":"UCbww426ub52iIAv3b6htZUA", "WIKI623737":"UCZsapl0PQ1dZ7pHYoBpRCow", "WIKI773158":"UCzIEUGSGIEiu9IK2Xuz1Knw", "WIKI38965354":"UC1-KikGbOHzGpZ-o7iIlsJw"}

channel_dict = {"OVP100019" : "UCYzPXprvl5Y-Sf0g4vX-m6g", "OVP100020" : "UCGjylN-4QCpn8XJ1uY-UOgA", "OVP100021" : "UCWRV5AVOlKJR1Flvgt310Cw", "WIKI12541729" : "UC3J6rj3T_t0cr5dQLEd40jg" , "WIKI542214" : "UCPC0L1d253x-KuMNwa05TpA", "OVP100022" : "UCWubgylxmhL9BQvwqeN1KNA"}

insert_query = 'insert ignore into smarttag_overrides (source_id, sk, gid, title, is_right) values ("%s", "%s", "%s", "%s", 1)'
select_clips = 'select clip_sk from ChannelClip where channel_sk = "%s" and clip_sk in (select sk from Clip)'
channel_title = 'select title from Channel where sk = "%s"'
for gid, channel_sk in channel_dict1.iteritems():
	try:
		if channel_sk == "UC30ar4xgM8qm78A5SNbneSg":
			title = "Hotline Bling"
		elif channel_sk == "UCtUF5knabzU3gf6pJ_EdTEw":
			title = "Crank That (Soulja Boy)"
		elif channel_sk == "UCzwzVFgZa3AS9IPLPfJjf1w":
			title = "Lindsay Stirling"
		else:
			cur.execute(channel_title % channel_sk)
			title = cur.fetchall()[0][0]
		cur.execute(select_clips % channel_sk)
		rows = cur.fetchall()
		for row in rows:
			clip_sk = row[0]
			cur.execute(insert_query % ('youtube', clip_sk, gid, title))
	except:
		print channel_sk	
		import pdb;pdb.set_trace()
		continue


cur.close()
'''
smart_tags = {'WIKI256004' : ["va_9a0daa86c9da4d6a9842b9a845a01345","va_1a1ac079efa94811ae472f2c46f364c7","va_5b55c6be4d214fe4b5356fda8c80e834","va_fd25c15cbb904be3a4aed3027125ec32","va_3c0ed0d9ee6948c58898db8cd4630656","va_324331b26a904a44b4fd44aa569f707f","va_815bb7a1c64f4b368ad7099a164175f3","va_b0c1498648c44b6bbd274d1665ec02af","va_4670396772b240df8d59137b26ea11a7","va_07e412b693304b129a15a067649f594e","va_465d7b3488a348f5934f102e1f4f3cf0","va_7e168ccc54244db48d76c7ff8610b006","va_fa11f99c8fc8461d8dc27f16d64133a6","va_902e0ead2b9c4ecca77dcfe112df3090","va_c4d6a19fae7048eba0bae7f08a2f9bb3","va_1acb47e39a9546be93767f3bd670f646","va_75b33572b09844c28836b1a8af1c6a96","va_b01246aec5c3457ab405bc53367b6c8b","va_d300f89c74954388997536893231ce89","va_d613f2e2dac046e5a500442aeccbd55b","va_f845c01a822a41969eccef99e60fd0a0","va_c899665f3e7941648916710cc07e0013","va_90eacef37ab642aebafa056bd7f2ed8b","va_7b4b2901b15749caa3e1bfc25b24e59c","va_feb9533547664e83956d94efc28bbc6e","va_d01be100f2f14b8d93bab597ac9eb0ba","va_f64822e744024a0caac0b74e419c13cb","va_ebb3ae0cce7f4995b81bf05df5222069","va_6639d2801b604a0f9d6d8a0b44c20b0f","va_a8790a42b8ad4767b7b139081a6fdfc5","va_1239d9ee16ea4ce99c238873fe131d4c","va_cde3dc69d20c441294d631b43746b236","va_5bf89c49011e47ac825dfd020a3e2ff2","va_4c9c50e9826a4c798109e58cc89ee332","va_ddae9997384745299776fea4408c0b42","va_f93db4a359eb408c8a8f37317fba67f3","va_2ac36420c64645609b92d1e9258d1bc9","va_78fe7889c9a64bf8a6f7caccd586d1c5","va_1322b5129d5849b89a2a3dc8d066658e","va_fcf9abc162914a2a90918cc91cebd1ac","va_1ef1b66a51b2415bb7b1074d5b9d3584","va_3d812c72ccce42c7a56781b14236a3b5","va_ac9fc7f894f647309758049dba2a026e","va_c03762c7c2c64d45b8362eb1ea1d2682","va_33eb8069883142c8991fbd05f6fc279c","va_727810e33453420da8dd8a0761268ab6","va_2d8f92156f4d487eaca0bfedfa5ca4f0","va_1e5888c624894070889e903bb105b4ab","va_fb6efa37443c466dbac463381e5455cb","va_5000ad9df5e9400b97726d32c963cf05","va_64d8de41c0394640a036d4ca584f9d31"]}

smart_tags = {'OVP100026' : ["va_bdb1af6149f246f087182258b1dc06e3", "va_674c065df1dd4445bae26fae61a70b54", "va_d7f4e765b9c443e9b0231f46705ced08", "va_789fd219c0cc49e5abded2dc2d239e88", "va_ef1b361bda104d3e945008b2ab71dc34", "va_2542ff0a74c1404b899cdb46fc318ee2", "va_989c43d449fb431398492682195c9eb1"]}

smart_tags= {'OVP100025' : ["va_c43570da5ac7429daaf61539993965b5", "va_277c53cbde5042cf80e54520093ca711", "va_e041bafe9aca457688ccb75d05430eb2", "va_db0bc5bad6ff48d988358356415804a9", "va_5aff37aa5df34bf7a4334041b037aace", "va_a9bd44b59221443a8106b5f1b464fd55", "va_90552b66319449d39959aa5ad3c3c15f", "va_3978a135cd46492a839bd60bfe2e7c4c", "va_471463d037f44aa6bcbb30cde9189f9a", "va_6a2fd9734840400594d3d2c1167db155", "va_f8e945b2066f4003bb72f7e26d54e219", "va_74037195f0ec481c9bcc5a95a83e8151", "va_6e3e43874ce1461ca5f214a24c6b4f42", "va_693d15f4610d47dbb95b2d13d26d075a", "va_c14936fa44b14a28a98f482b51a555db", "va_9db1a501f9ff469a941c9abc8787e606", "va_d020772c46e045f9b0e30bf51060ef6e", "va_9ea08f470ea24fa38895b76f7b7be043", "va_fea8053ff44b442099c5097c4e30fdb5", "va_20c6c52093c742b692c99735f814de65", "va_723b27316e18497a8f5649bfb0e07f02", "va_9dc0458170b34c0687156672cde0a732", "va_43155d5c75fd47d09ce58eafeabfcc5f", "va_d79018048bfd4551be5b741696c5d031", "va_0b2de769eab44c1c8063ab49e95825f9", "va_40d1179c992248c8899192d7cfc95a2f", "va_e3a59f1f8d4445b8853d055184ac4b76", "va_2f87ab19c45a446e8980e88a2da6619b", "va_77e711006bdb4dddb3cd2bad7ad6b61a", "va_fe0b16050f3548d484535ddef635edca", "va_c7a5d3a33055497099cd1897348ee13c", "va_f20d316fd1264a90a5317236e9934672", "va_53f20f6feb3b4c29877ae2bd19993535", "va_c9710842ca184d9a8a66cb130bba2c30", "va_f5a680dba09b47d3b5cda4ccddc2a7de", "va_a864496db4a34630a7c6b1f86b5f687f", "va_3ff21f07e9a4487d86ce3ed59834fbf4"]}

smart_tags = {'WIKI34909431' : ["va_4d29e41edd0d42dfad2cf519f5c3ba45", "va_59916d0ff9a9452cb33891a5e35ba56a", "va_cd5b4a3b0f2c49ec8942e64175d13b07", "va_72e6b671b5ee4986a404901ca70729c3", "va_bb044fe881d54b86bb6373c9e7c1e76f", "va_ee55c45d404845ec9600030d1db627d3", "va_3154c7884b8647caaab85a72402640b2", "va_bf078201d8e04577b48a3ef30c119d7d", "va_6ed88fef1d0549508abb6412ac6443d9", "va_ce9fb90bbd0841849369f7c8f1652f5e", "va_d6334d4a235d4cab85eb85b2bbc2b724", "va_f01be07053a740a9b43a18646be7856e", "va_0f207b7a8793468a8908a7f3a6f88ff6", "va_c3707c2c6c584591a431be150712ce16", "va_266fdaedc9d441479c31d6eb90f7b406", "va_163da60b6be24b83975d0b5fe9b72813", "va_cd174932376b45709f16787d58bd25a7", "va_b90f2232f6f648518b7e60a4913e9e73", "va_e29343b0324a4d0ba55a7919d69492a1", "va_f07c15b0b6a84a398245d6b9657770ea", "va_8de4142dc1064bc2bab726a07ac819c2", "va_600fab6b0bf2450fb4159793e98f8233", "va_a7c94230dc0b477caa59b5b647d9cab5", "va_85e034db23314f7f9ea800f99ba43946", "va_3abb631597e243728b20593dcf86ffbf", "va_ee4c217feff74ed999d445c6a7e9e9ea", "va_71fcec9f8c044b79a9cdccd3bc1dda41", "va_b300533f3df640c5a1705f9ea6670779", "va_b9166ca9f46f4ebc9ad05deaff9954ba", "va_3efccd8773474e24ad5e00cd698a8cbf", "va_3056648d5d59429f86598c8fed8183d2", "va_81038558f4b34350b0743520df25e29c", "va_d6f55d3b1c3b45e182f6dc5da9712bc0", "va_32547b9cb0c841ae88fa42fbf5f54f35", "va_4844439f37a24f13b211f7c7905444f1", "va_7b19d185edb044048cd349e875cf3e9a", "va_5d4d36cd37504a5d85f0761633ff1bb5", "va_d5cbe8d41c324227a374ee58d6552467", "va_e341eaabde2b47fdac8dc383fb7033e6", "va_c4ca6d808d87481e82198b248a99d69f", "va_709c0d7e88ce496fad572761fc7b1814", "va_edb81ca32e1642b89033a7ef92c0d406"]}


smart_tags= {'OVP100026' : ["_riJrU4OJuo","_TRvafcqhzc","--sd88g6eXA","0q59S1TsZHQ","1nblzC7ew0I","1TWIvEyO_5I","1yWueg4zQX8","3fwRi1uuG3U","47pAVaP_vfs","4tlefunjimg","7-tirQwabC4","7Y8nBCyooRI","8H-ulYE8Apg","91W4Dd5xcsM","9lxDyO4312Y","a3hW8HYQYEk","B9syyBeHymQ","BAlEdFNBOy0","bsu4fZ0qV5I","bU4E7o5NOsE","BZu3tW_K9a8","c2P-UmjCp8I","e24r1ZSRxqk","en7JV4pXxVs","f-caXi7H92U","Fm4f0Ut1JvM","HEnj0BC11KQ","IJ_Sk6k6UZc","inVog4cs_10","ioWzlYuj2IQ","jChd94e82g0","Jt9t1udhvc4","jw6zPaoWtuY","kCzFFNWk6Hg","KJqmPdBtZjs","kzi710gHQqE","L6GEyNBx294","Msov6g9zThI","NL6XoreUfco","nP_CXF2cXUE","NTtats4juPU","nylTHQJsrz4","OhtdlgWnBcI","OMRkbhsOKSI","OwNYIww709Q","Oxmbot2ZGAc","pUcBDEydaW8","PWjkEM1pd2Y","s-B4QDszIpU","svk4vXoz8pw","U3vp5kGVIr0","U4mRzX81pkg","uBWrpVrazzA","uR8HqmABCpA","vaXeeeq5QLA","vbuNWd7qiss","Vu-NVonQiuc","vybDhF2bONI","w2jXMzUX0Vo","wB3g1C4VUX8","wOMipoB1gpk","WzeS2mgiLOI","XDjjmQi04YM","Xq80D1kpZ6c","XytJd38UBwU","yVLq153EH44","ZNOiiWPx3Ic","ZSNCA3J_KWc","ZvdjFSrce7I","zvL-GsuiEj8"]}


smart_tags = {'OVP100029' : ["va_7ddf6946e97a4facb371f47f96693258","va_778ce18e22084f09aebd5a5a510ff140","va_56cbdfd8be384deb828b099eb60a9ee4","va_a3471f18a8eb43ca9eb797dc5ac291ac","va_9e5b05aac29a4cec8811ef166bfb6baf","va_3325a3e64449488f8d96286d0c0c6824","va_3723c53997ca4babb63b901f12860f8d","va_c007696c1fd246458375b9a25289ffd4","va_c627f5b180e9482a9b5bdcba745669c0","va_c51b1e2305244f24b59f7c42b3d75b81","va_1bf6c94135a94281a88031bd69c34f1e","va_b248347fb4d7454394ec2c1f0ad46b51","va_abb3ad47eaa04324a008560d2e475ecb","va_21a7918175d64078bfbfaf4209202af2","va_191ff01637974fd38e8cb401f316917c","va_18cb3a3507754346a1c42f220eb9d7f4","va_1400e4a220d74e3f9778de8973a76cf9","va_ec9f026bcc3947f9adcc533aa8c70abc","va_66e5adcea30943bfaf1de9a483fce3d7","va_bbbee91c4b0b463da8b43426f2b95d59","va_46ec9c30540546eea29a6531cf83cded","va_ca5354e29a6040a48b31164716e4bc5d","va_c64a6f6c03774faa8ec7c7a052bf720d","va_a117f8cdc5ea43afa9f8f58e8e61f01d","va_22d9177106bb473f96e31bd0324da53a","va_2f6d23666d6c40de82d46a63b8ec3950","va_49ec36d510a24ca484e8623f26bfc4b0","va_873e5428241c4adf8872768ce38f5398","va_c76a4211e8024741bacb077667bb5a6c","va_30d16b0f97f7425bbfdf53f29d95a344","va_a8df891c14674cad9d1f91aea02df0af","va_e67b99b16a2c497f835ab8a060fc878c","va_b16e2673978b4f88b8de47878b1ca209","va_8ac94341dcf44d0c91a70ea61c77202b","va_07bab926135b40b1bb6bf2e1edd31e06","va_24fd499e9ce947d3b2b30049c5121b0f","va_a33e60e0cca3453a9b4519ccdb3373a8","va_c172cb26d32f41efac35a83bf3d0d978","va_e7d0d33500064b0cae73363a903cdfa8","va_ca6f045e750b440886dec843f6c73c64", "va_7a96eded37304da6a3a379b657030824"]}

insert_query = 'insert ignore into smarttag_overrides (source_id, sk, gid, title, is_right) values ("%s", "%s", "%s", "%s", 1)'
cur.execute(insert_query % ('go90', 'va_c172cb26d32f41efac35a83bf3d0d978', 'OVP100036', "Venus X"))
cur.execute(insert_query % ('go90', 'va_b248347fb4d7454394ec2c1f0ad46b51', 'OVP100035', "Wilson Tang"))
cur.execute(insert_query % ('go90', 'va_9e5b05aac29a4cec8811ef166bfb6baf', 'OVP100034', "Johnny Huynh"))
cur.execute(insert_query % ('go90', 'va_e67b99b16a2c497f835ab8a060fc878c', 'OVP100033', "Bryce Shuman"))
cur.execute(insert_query % ('go90', 'va_c76a4211e8024741bacb077667bb5a6c', 'OVP100032', "Julien Ehrlich"))

'''
cur.execute(insert_query % ('go90', 'va_18cb3a3507754346a1c42f220eb9d7f4', 'WIKI38194124', "ASAP Ferg"))
cur.execute(insert_query % ('go90', 'va_e7d0d33500064b0cae73363a903cdfa8', 'WIKI47010161', "Jackie Cruz"))
cur.execute(insert_query % ('go90', 'va_46ec9c30540546eea29a6531cf83cded', 'WIKI24230625', "Tinie Tempah"))
cur.execute(insert_query % ('go90', 'va_07bab926135b40b1bb6bf2e1edd31e06', 'WIKI47288767', "Alex G"))
cur.execute(insert_query % ('go90', 'va_bbbee91c4b0b463da8b43426f2b95d59', 'WIKI38246480', "Willie Cauley-Stein"))
cur.execute(insert_query % ('go90', 'va_bbbee91c4b0b463da8b43426f2b95d59', 'WIKI38246480', "Willie Cauley-Stein"))
cur.execute(insert_query % ('go90', 'va_a33e60e0cca3453a9b4519ccdb3373a8', 'WIKI47075424', "Bully"))
cur.execute(insert_query % ('go90', 'va_1400e4a220d74e3f9778de8973a76cf9', 'WIKI22998059', "Nigel Sylvester"))
cur.execute(insert_query % ('go90', 'va_24fd499e9ce947d3b2b30049c5121b0f', 'WIKI32779348', "Vince Staples"))
cur.execute(insert_query % ('go90', 'va_ca6f045e750b440886dec843f6c73c64', 'WIKI1701874', "Tiga"))
cur.execute(insert_query % ('go90', 'va_ec9f026bcc3947f9adcc533aa8c70abc', 'WIKI50955519', "D.R.A.M."))
cur.execute(insert_query % ('go90', 'va_66e5adcea30943bfaf1de9a483fce3d7', 'WIKI22699475', "Rene Redzepi"))
cur.execute(insert_query % ('go90', 'va_3723c53997ca4babb63b901f12860f8d', 'WIKI35761776', "Bubba Wallace"))
cur.execute(insert_query % ('go90', 'va_2f6d23666d6c40de82d46a63b8ec3950', 'WIKI46252498', "Halsey"))
cur.execute(insert_query % ('go90', 'va_abb3ad47eaa04324a008560d2e475ecb', 'WIKI19671800', "Joby Ogwyn"))
cur.execute(insert_query % ('go90', 'va_49ec36d510a24ca484e8623f26bfc4b0', 'WIKI31737939', "Ty Dolla $ign"))
cur.execute(insert_query % ('go90', 'va_c627f5b180e9482a9b5bdcba745669c0', 'WIKI6260337', "Eric Kelly"))
cur.execute(insert_query % ('go90', 'va_22d9177106bb473f96e31bd0324da53a', 'WIKI2855123', "Eleanor Friedberger"))
cur.execute(insert_query % ('go90', 'va_778ce18e22084f09aebd5a5a510ff140', 'WIKI13213495', "Carmelita Jeter"))
cur.execute(insert_query % ('go90', 'va_3325a3e64449488f8d96286d0c0c6824', 'WIKI1799831', "Ben Weinman"))
cur.execute(insert_query % ('go90', 'va_30d16b0f97f7425bbfdf53f29d95a344', 'WIKI36577373', "Daryl Homer"))
cur.execute(insert_query % ('go90', 'va_a8df891c14674cad9d1f91aea02df0af', 'WIKI47802632', "Bibi Bourelly"))
cur.execute(insert_query % ('go90', 'va_c007696c1fd246458375b9a25289ffd4', 'WIKI17066786', "Jonathan Mannion"))
cur.execute(insert_query % ('go90', 'va_56cbdfd8be384deb828b099eb60a9ee4', 'WIKI47805110', "Kerby Jean-Raymond"))
'''
#cur.execute(insert_query % ('youtube', 'srtLGgawxKA', 'WIKI47010161', "Jackie Cruz"))

clips = 'select sk from Clip where sk in (select clip_sk from ChannelClip where channel_sk = "%s")' % "UCsjrSi7xMkKPk4gcLSjFKbA"
cur.execute(clips)
rows = cur.fetchall()
for row in rows:
	insert_query = 'insert ignore into smarttag_overrides (source_id, sk, gid, title, is_right) values ("%s", "%s", "%s", "%s", 1)'
	values = ('youtube', row[0], 'WIKI38194124', 'ASAP Ferg')
	#cur.execute(insert_query  % values)

clip_sks = ['hxH6bKNPBIA', 'UuL27DzHFP4', 'JUWSLlz0Fdo', '-kjyltrKZSY', 'qVMW_1aZXRk', '-nQGBZQrtT0', 'Kbryz0mxuMY', 'Qsvy10D5rtc', 'yxD5QkzmVOA', 'VTcrztNxI-c', 'akOpXknRIQk', '4CVTuOyZDI0&t=40s', 'Z73H5urfx-c', 'jB2zoidUeLU', 'zi_tuMjl8DY', '4SjeD_GR-UM', '7BEieHKxiaE']

for clip_sk in clip_sks:
	insert_query = 'insert ignore into smarttag_overrides (source_id, sk, gid, title, is_right) values ("%s", "%s", "%s", "%s", 1)'
	values = ('youtube', clip_sk, 'WIKI4848272', 'Donald Trump')
	cur.execute(insert_query  % values)
cur.close()
conn.close()

