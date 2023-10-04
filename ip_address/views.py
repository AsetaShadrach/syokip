import logging
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from services.utils import AutoCreateIps
from .models import IpAddress,IpStatus

logger = logging.getLogger('backend')

class AllocateIp(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        logging.info({**request.data})
        data  = request.data
        using_released_ip = False

        try:
            # if data.get('auto'):
                # If passed with auto , auto create IP
            allocated_ip_adresses = IpAddress.objects.filter(status =IpStatus.ALLOCATED.value)
            if allocated_ip_adresses.count() < 1:
                logging.info(f"Initiating ip allocation from init ip")   
                ip = '198.162.1.9'
            else:
                unall_ip_adresses = IpAddress.objects.filter(status =IpStatus.UNALLOCATED.value)
                # If there is an IP that was released
                if unall_ip_adresses.count() > 1:
                    logging.info(f"Initiating ip allocation from released IP")   
                    using_released_ip = True
                    un_ip = unall_ip_adresses.first()
                    ip_ = [int(n) for n in un_ip.ip.split('.')]
                    ip_[-1] = ip_[-1]-1
                    ip = '.'.join([str(ip_part) for ip_part in ip_])
                    
                else:
                    # If no IP has been released continue from last allocated
                    ip = allocated_ip_adresses.latest('created_at').ip

            logging.info(f"Initiating ip allocation from last IP,{ip}")           
            ip_auto_creator = AutoCreateIps()
            ip_auto_creator.generate_from_last_ip(ip, 1)
            generated_ip = ip_auto_creator.list_of_ips[1]
            
            if using_released_ip:
                ip = un_ip
                ip.is_active = True
                ip.status = IpStatus.ALLOCATED.value
                ip.customer_name = data.get('customer_name')
                ip.email = data.get('email')

            else:
                ip = IpAddress(
                    **data,
                    ip=generated_ip,
                    is_active=True,
                    status = IpStatus.ALLOCATED.value
                )

            ip.save()   

            return Response(
                    data={
                        'status':status.HTTP_201_CREATED,
                        'response': f'IP {ip.ip} succesfully allocated', 
                        'responseDescription': 'IP(s) succesfully allocated'
                        },
                    status=status.HTTP_201_CREATED
                )               
           
        except Exception as e:
            logging.error(e)
            return Response(
                    data={
                        'status':status.HTTP_500_INTERNAL_SERVER_ERROR,
                        'response': str(e), 
                        'responseDescription': str(e)
                        },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )


    def put(self, request, *args, **kwargs):
        ip = IpAddress.objects.filter(ip=kwargs.get("ip"), status=IpStatus.ALLOCATED.value).first()
        if not ip:
            return Response(
                status=404,
                data={
                    "message": "IP not found",
                    "error": "IP address not found ",
                    "responseDescription": f"No ip : {kwargs.get('ip')}",
                },
            )

        
        ip.status=IpStatus.ALLOCATED.value
        ip.is_active=False
        ip.save()
        return Response(status=200, 
            data={
                'status':status.HTTP_200_OK,
                'response':f'IP successfully released',
                'responseDescription': f'{ip.id} tied to IP {ip.ip} has been released'
                })
        

    
    
class GetAllocatedIps(APIView):
    serializer_class = serializers.IpAddressSerializer

    def get(self, request, *args, **kwargs):
        logging.info('fetching all allocated IPs')
        return self.get_queryset(self, request, *args, **kwargs)

    def get_queryset(self, request, *args, **kwargs):
        logging.info('fetching all allocated IPs queryset')

        try:
            queryset = IpAddress.objects.filter(status =IpStatus.ALLOCATED.value)
        
            return Response(
                status=status.HTTP_200_OK,
                data={
                    'status': status.HTTP_200_OK,
                    'response':{
                        'count':queryset.count(),
                        'data': serializers.IpAddressSerializer(queryset,  many=True).data,                    
                        },
                    'responseDescription': 'IP fetch complete'
                }
            )
        except Exception as e:
            logging.error(e)
            return Response(
                    data={
                        'status':status.HTTP_500_INTERNAL_SERVER_ERROR,
                        'response': str(e), 
                        'responseDescription': str(e)
                        },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        
    
class GetAvailableIps(APIView):
    serializer_class = serializers.IpAddressSerializer

    def get(self, request, *args, **kwargs):
        logging.info('fetching all available IPs')
        try:
            ip = IpAddress.objects.filter(status=IpStatus.ALLOCATED.value).latest('created_at')  
            logging.info(f"Geting available IPs from las available ip {ip}")  
            ip_auto_creator = AutoCreateIps()    
            ip_auto_creator.get_available_ip_addresses(ip)
            available_ips= ip_auto_creator.list_of_ips

            return Response(
                status=status.HTTP_200_OK,
                data={
                    'status': status.HTTP_200_OK,
                    'response':{
                        'count': len(available_ips),
                        'ips': available_ips,                    
                        },
                    'responseDescription': 'User fetch complete'
                }
            )
        except Exception as e:
            logging.error(e)
            return Response(
                    data={
                        'status':status.HTTP_500_INTERNAL_SERVER_ERROR,
                        'response': str(e), 
                        'responseDescription': str(e)
                        },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

