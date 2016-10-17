#encoding=utf8
import MySQLdb, urllib, urllib2, json, time, sys

url = "http://api.map.baidu.com/place/v2/search"
url_default = "&ak=M7sDWVlmcSWnot4AOMoq0wLO&output=json&page_size=1&page_num=0&scope=1"

def main():
	#req = urllib2.Request(url+'?'+"city=beijing&"+my_api_key)
	insertIntoDB();

def insertIntoDB():
	try:
		conn = MySQLdb.connect(
			host = 'localhost',
			user = 'root',
			passwd = 'root',
			db = 'sdweather',
			charset = 'utf8'
			)
		cur = conn.cursor()
		cur.execute("select * from station")
		results = cur.fetchall()
		for r in results:
			area = r[1]
			name = r[2]
			url_search = "&query="+name.encode('utf8')+"&region="+area.encode('utf8')
			#print url_search
			if name.encode('utf8')=='22中南校区':
				url_search = "&query="+'22中'+"&region="+name.encode('utf8')
			req = urllib2.Request(url+'?'+url_default+url_search);
			resp = urllib2.urlopen(req)
			content = resp.read()
			if not content:
				continue
		
			data = json.loads(content)
			#print data		
			iid = "update station set lat = %s, lng = %s where name = %s and area = %s"
			tmp = data['results']
			if not tmp:
				continue
			s = tmp[0]
			print s
#			print '1111'
			values = []
			if 'location' in s:
				aa = s['location'];
				values.append(aa['lat'])
				values.append(aa['lng'])
				values.append(name)
				values.append(area)
				cur.execute(iid, values)
		cur.close()
		conn.commit()
		conn.close()
		print "Successed"

	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])
	except IndexError, e:
		print 'ss'

if __name__ == '__main__':
	main()
