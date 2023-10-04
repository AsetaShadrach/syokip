import logging
logger = logging.getLogger('backend')

class AutoCreateIps():
    def generate_ips_from_range_diff(self,
        level1:int=0, level2:int=0, 
        level3:int=0, level4:int=0,
        level1_diff:int=0, level2_diff:int=0, 
        level3_diff:int=0, level4_diff:int=0):

        list_of_ips = [str(ipmap)+'.' for ipmap in range(level1, level1+level1_diff+1 )]
        list_of_ips = [ x+f'{y}.' for x in list_of_ips for y in range(level2, level2+level2_diff+1)]
        list_of_ips = [ x+f'{y}.' for x in list_of_ips for y in range(level3, level3+level3_diff+1)]
        list_of_ips = [ x+f'{y}' for x in list_of_ips for y in range(level4, level4+level4_diff+1)]
        
    
        logger.info(f'List of generated IPS : {list_of_ips}')
        self.list_of_ips = list_of_ips

        return list_of_ips



    def generate_from_ip_range(self, ip1:str,ip2:str):
        ip1_ = [int(n) for n in ip1.split('.')]
        ip2_ = [int(n) for n in ip2.split('.')]
        info = {}

        for ind,item in enumerate(zip(ip1_,ip2_)):
            info['level'+f'{ind+1}'] = min([item[0],item[1]])
            info['level'+f'{ind+1}_diff'] = max([item[0],item[1]]) - min([item[0],item[1]])

        logger.info(f'Creating IPs using info :: {info}')

        self.generate_ips_from_range_diff( 
            info['level1'], info['level2'], info['level3'], info['level4'], 
            info['level1_diff'], info['level2_diff'], info['level3_diff'], info['level4_diff']
        )
            
    
    def generate_from_last_ip(self, last_ip, count):
        if last_ip:
            if isinstance(last_ip,str):
                ip = last_ip
            else:
                ip = last_ip.ip
        else:
            # This is a placeholder the IP could be anything
            ip = '198.162.1.10'
        
        ip_ = [int(n) for n in ip.split('.')]

        # for now only restrict to max 0f ip '198.162.1.20'
        if ip_[-1]+count >20:
            raise InterruptedError('No IPs are available')

        if ip_[-1]+count > 255:
            ip_[-2] = ip_[-2]+1
            ip_[-1] = ip_[-1]+count - 255
        else:
            ip_[-1] = ip_[-1]+count

        second_ip = '.'.join([str(ip_part) for ip_part in ip_])
        
        logger.info(f'Initiating new ip creation with {ip}, {second_ip}')
        self.generate_from_ip_range(ip, second_ip)


    def get_available_ip_addresses(self, last_ip):
        if last_ip:
            ip_l = last_ip.ip.split('.')
            ip_l[-1] = str(int(ip_l[-1]) + 1)
            ip = '.'.join(ip_l)

        else:
            # This is a placeholder the IP could be anything
            ip = '198.162.1.10'
        self.generate_from_ip_range(ip, '198.162.1.20')



