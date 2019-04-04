# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK
from rest_framework import viewsets

import subprocess
import getpass
import requests
import json

from .models import *
from .serializers import *

WALLET_API_URL = "http://127.0.0.1:"
WALLET_API_PATH = "/api/wallet"


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    @staticmethod
    def list(request, *args, **kwargs):
        wallets = Wallet.objects.all()
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def create_address(request):
    port = request.GET['port']
    r = requests.post(WALLET_API_URL + port + WALLET_API_PATH,
                      json={'jsonrpc': '2.0',
                            'id': 1,
                            'method': 'create_address',
                            'params': {
                                'lifetime': 24
                            }})
    result = json.loads(r.text)

    return Response(result['result'], status=HTTP_200_OK)

@api_view(['GET'])
def edit_address(request):
    port = request.GET['port']
    address = request.GET['address']
    comment = request.GET['comment']
    expiration = request.GET['expiration']
    r = requests.post(WALLET_API_URL + port + WALLET_API_PATH,
                      json={'jsonrpc': '2.0',
                            'id': 8,
                            'method': 'edit_address',
                            'params': {
                                'address': address,
                                'comment': comment,
                                'expiration': expiration
                            }})
    result = json.loads(r.text)

    return Response(result['result'], status=HTTP_200_OK)


@api_view(['GET'])
def delete_address(request):
    port = request.GET['port']
    address = request.GET['address']

    r = requests.post(WALLET_API_URL + port + WALLET_API_PATH,
                      json={'jsonrpc': '2.0',
                            'id': 8,
                            'method': 'delete_address',
                            'params': {
                                'address': address
                            }})
    result = json.loads(r.text)

    return Response(result['result'], status=HTTP_200_OK)


@api_view(['GET'])
def get_wallet_status(request):
    port = request.GET['port']
    r = requests.post(WALLET_API_URL + port + WALLET_API_PATH,
                      json={'jsonrpc': '2.0', 'id': 6, 'method': 'wallet_status'})
    result = json.loads(r.text)

    return Response(result['result'], status=HTTP_200_OK)


@api_view(['GET'])
def get_utxo(request):
    port = request.GET['port']
    r = requests.post(WALLET_API_URL + port + WALLET_API_PATH,
                      json={'jsonrpc': '2.0', 'id': 7, 'method': 'get_utxo'})
    result = json.loads(r.text)

    return Response(result['result'], status=HTTP_200_OK)


@api_view(['GET'])
def get_addr_list(request):
    port = request.GET['port']
    r = requests.post(WALLET_API_URL + port + WALLET_API_PATH,
                      json={'jsonrpc': '2.0', 'id': 8, 'method': 'addr_list', 'params': {'own': True}})
    result = json.loads(r.text)

    return Response(result['result'], status=HTTP_200_OK)


@api_view(['GET'])
def get_contacts_list(request):
    port = request.GET['port']
    r = requests.post(WALLET_API_URL + port + WALLET_API_PATH,
                      json={'jsonrpc': '2.0', 'id': 8, 'method': 'addr_list', 'params': {'own': False}})
    result = json.loads(r.text)

    return Response(result['result'], status=HTTP_200_OK)


@api_view(['GET'])
def get_tx_list(request):
    port = request.GET['port']
    r = requests.post(WALLET_API_URL + port + WALLET_API_PATH,
                      json={'jsonrpc': '2.0', 'id': 8, 'method': 'tx_list'})
    result = json.loads(r.text)

    return Response(result['result'], status=HTTP_200_OK)


@api_view(['GET'])
def tx_send(request):
    port = request.GET['port']
    fee = request.GET['fee']
    from_address = request.GET['from']
    to_address = request.GET['address']
    comment = request.GET['comment']
    value = request.GET['value']
    r = requests.post(WALLET_API_URL + port + WALLET_API_PATH,
                      json={'jsonrpc': '2.0',
                            'id': 2,
                            'method': 'tx_send',
                            'params': {
                                'value': int(value),
                                'fee': int(fee),
                                'from': from_address,
                                'address': to_address,
                                'comment': comment
                            }})
    result = json.loads(r.text)
    return Response(result['result'], status=HTTP_200_OK)


@api_view(['GET'])
def tx_swap(request):
    address = request.GET['address']
    amount_beam = request.GET['amount_beam']
    amount_btc = request.GET['amount_btc']
    subprocess.call("beam-wallet --wallet_path=\"wallet.db\" "
                    "-n eu-node01.masternet.beam.mw:8100 swap_coins "
                    " --amount " + amount_beam + " --fee 100 "
                    "-r " + address +
                    " --pass=123 --swap_amount " + amount_btc +
                    " --swap_beam_side "
                    "--btc_node_addr 127.0.0.1:13300 "
                    "--btc_pass 123 "
                    "--btc_user Alice", shell=True)
    return Response('Completed successfully', status=HTTP_200_OK)


@api_view(['GET'])
def tx_cancel(request):
    port = request.GET['port']
    tx_id = request.GET['tx_id']
    r = requests.post(WALLET_API_URL + port + WALLET_API_PATH,
                      json={'jsonrpc': '2.0',
                            'id': 4,
                            'method': 'tx_cancel',
                            'params': {
                                'txId': tx_id
                            }})
    result = json.loads(r.text)

    return Response(result['result'], status=HTTP_200_OK)
