from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from leaderboard.models import leaderboard_user
from rest_framework.test import RequestsClient
from requests.auth import HTTPBasicAuth
from rest_framework.test import force_authenticate
from django.contrib.auth import get_user_model
import json


class LeaderBoardUserTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test',
            'test@test.com',
            'test',
        )
        self.list_url = reverse('leaderboard-list')
    
    def test_unauthenticated_create_user(self):
        response = self.client.post(self.list_url, data={
            'name': 'TestName',
        })
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_create_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, data={
            'name': 'TestName',
            'age': 1,
            'address': 'test address'
        })
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            leaderboard_user.objects.first().name,
            'TestName',
        )

    def test_get_user(self):
        self.client.force_authenticate(user=self.user)
        user_data = {
            'name': 'TestName',
            'age': 1,
            'address': 'test address'
        }
        self.client.post(self.list_url, data=user_data)
        self.detail_url = reverse('leaderboard-detail', kwargs={'pk': 1})
        response = self.client.get(self.detail_url)
        result = json.loads(response.content)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            result['name'],
            user_data['name'],
        )
        self.assertEqual(
            result['age'],
            user_data['age'],
        )
        self.assertEqual(
            result['address'],
            user_data['address'],
        )

    def test_get_user_not_found(self):
        self.client.force_authenticate(user=self.user)
        user_data = {
            'name': 'TestName',
            'age': 1,
            'address': 'test address'
        }
        self.client.post(self.list_url, data=user_data)
        self.detail_url = reverse('leaderboard-detail', kwargs={'pk': 2})
        response = self.client.get(self.detail_url)
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_update_user(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(self.list_url, data={
            'name': 'TestName',
            'age': 1,
            'address': 'test address'
        })
        self.detail_url = reverse('leaderboard-detail', kwargs={'pk': 1})
        updated_data = {
            'name': 'TestNameUpdated',
            'age': 2,
            'address': 'test addressupdated'
        }
        response = self.client.put(self.detail_url, data=updated_data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            leaderboard_user.objects.first().name,
            updated_data['name'],
        )
        self.assertEqual(
            leaderboard_user.objects.first().age,
            updated_data['age'],
        )
        self.assertEqual(
            leaderboard_user.objects.first().address,
            updated_data['address'],
        )
    
    def test_delete_user(self):
        self.client.force_authenticate(user=self.user)
        user_to_delete = self.client.post(self.list_url, data={
            'name': 'TestName',
            'age': 1,
            'address': 'test address'
        })
        self.detail_url = reverse('leaderboard-detail', kwargs={'pk':1})
        response = self.client.delete(self.detail_url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        user_exists = leaderboard_user.objects.filter(pk=1)
        self.assertFalse(user_exists)

class LeaderBoardPointsTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test',
            'test@test.com',
            'test',
        )
        self.list_url = reverse('leaderboard-list')
    
    def test_unauthenticated_point_up(self):
        self.detail_url = reverse('leaderboard-detail', kwargs={'pk': 1})
        response = self.client.put(self.detail_url+'point_up/', data={})
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_point_up(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(self.list_url, data={
            'name': 'TestName',
            'age': 1,
            'address': 'test address'
        })
        self.detail_url = reverse('leaderboard-detail', kwargs={'pk': 1})
        response = self.client.put(self.detail_url+'point_up/', data={})
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            leaderboard_user.objects.first().points,
            1,
        )

    def test_unauthenticated_point_down(self):
        self.detail_url = reverse('leaderboard-detail', kwargs={'pk': 1})
        response = self.client.put(self.detail_url+'point_down/', data={})
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
    
    def test_point_down(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(self.list_url, data={
            'name': 'TestName',
            'age': 1,
            'address': 'test address'
        })
        self.detail_url = reverse('leaderboard-detail', kwargs={'pk': 1})
        ##adding 2 points before taking one out
        self.client.put(self.detail_url+'point_up/', data={})
        self.client.put(self.detail_url+'point_up/', data={})
        response = self.client.put(self.detail_url+'point_down/', data={})
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            leaderboard_user.objects.first().points,
            1,
        )
    
    def test_point_down_under_zero(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(self.list_url, data={
            'name': 'TestName',
            'age': 1,
            'address': 'test address'
        })
        self.detail_url = reverse('leaderboard-detail', kwargs={'pk': 1})
        response = self.client.put(self.detail_url+'point_down/', data={})
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            leaderboard_user.objects.first().points,
            0,
        )
    

