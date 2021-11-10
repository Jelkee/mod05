import unittest
from webserver.app import *
import random


class LoginTest(unittest.TestCase):

    def test_1_loginWithCorrectInfo(self):
        tester = app.test_client(self)
        res = tester.post('/login', data=dict(username="bob", password="bob"))
        self.assertEquals(res.status, "302 FOUND")  # test if it can redirect with the correct username and password
        self.assertEquals(res.location, 'http://localhost/home/0')  # test if it redirect to /home
        res_redirect = tester.post('/login', data=dict(username="bob", password="bob"), follow_redirects=True)
        self.assertEquals(res_redirect.status, "200 OK")  # test if the redirect succeeded

    def test_2_loginWithWrongInfo(self):
        tester = app.test_client(self)
        res = tester.post('/login', data=dict(username="test", password="testpassword"))
        print("wrong " + str(res))
        # self.assertRedirects(res, 'home', status_code=302)
        self.assertNotEquals(res.status, "302 FOUND")  # test


'''
light manually or automatically
'''


def reset_sessionID(sessionID):
    query = "delete from mod5.sessions where uid = " + sessionID


class DatabaseTest(unittest.TestCase):
    def test_1_insertquery(self):
        mock_sessionID = random.randint(0, 500)
        query = "insert into mod5.sessions(sessionid, uid) values(\'" + str(mock_sessionID) + "\',\'1\')"
        result = SQLqueryInsert(query)
        self.assertEqual("Succeeded!", result)
        reset_sessionID(str(mock_sessionID))

    def test_2_simpleSQLquery(self):
        query = "SELECT * FROM mod5.users"
        result = simpleSQLquery(query)
        self.assertIn("Stefan", str(result))
        self.assertIn("bob", str(result))
        self.assertIn("Toby", str(result))


class ComponentTest(unittest.TestCase):
    newCid = 0

    def test_1_fetchAllRooms(self):
        result = str(fetchAllRooms())
        self.assertIn("Living room", result)
        self.assertIn("Kitchen", result)
        self.assertIn("Master bedroom", result)

    def test_2_fetchAllComponent(self):
        result = str(fetchAllComponents())
        self.assertIn("Light in room1", result)
        self.assertIn("light1", result)

    def test_1_addComponentWithSid(self):
        testaddC = app.test_client(self)
        testaddC.post('/login', data=dict(username="Toby", password="Toby"))
        res = testaddC.post('/components/add', data=dict(name="Test", room="1", type="light", gpio=7))
        self.assertEquals(res.status, "302 FOUND")
        self.assertEquals(res.location, 'http://localhost/components')
        checkDB = str(fetchAllComponents())
        self.assertIn("Test", checkDB)
        query = "SELECT lightid FROM mod5.lights WHERE name = 'Test'"
        newComponentID = simpleSQLquery(query)
        print(newComponentID[0][0])
        ComponentTest.newCid = newComponentID[0][0]

    def test_2_editComponentWithSid(self):
        testeditC = app.test_client(self)
        testeditC.post('/login', data=dict(username="Toby", password="Toby"))
        res = testeditC.post('/components/edit/light/' + str(ComponentTest.newCid), data=dict(name="TestEdit",
                                                                                             room="1", gpio=13))
        dbRes = str(fetchAllComponents())
        self.assertIn("TestEdit", dbRes)

    def test_3_deleteComponentWithSid(self):
        testdelC = app.test_client(self)
        testdelC.post('/login', data=dict(username="Toby", password="Toby"))
        res = testdelC.get('/components/delete/light/' + str(ComponentTest.newCid))
        dbRes = str(fetchAllComponents())
        self.assertNotIn(str(ComponentTest.newCid), dbRes)


class UserManagementTest(unittest.TestCase):
    testUid = 0

    def test_1_FetchAllUsers(self):
        res = str(fetchAllUsers())
        self.assertIn("Stefan", res)
        self.assertIn("bob", res)
        self.assertIn("Toby", res)

    def test_2_AddUser(self):
        testaddU = app.test_client(self)
        testaddU.post('/login', data=dict(username="Toby", password="Toby"))
        res = testaddU.post('/users/add',
                            data=dict(username="test", password="Test123", type="user", email="yfsun2019@gmail.com"))
        dbRes = str(fetchAllUsers())
        self.assertIn("test", dbRes)
        self.assertIn("yfsun2019@gmail.com", dbRes)
        query = "SELECT uid FROM mod5.users WHERE username = 'test' AND email = 'yfsun2019@gmail.com'"
        selRes = simpleSQLquery(query)
        UserManagementTest.testUid = selRes[0][0]

    def test_3_editUser(self):
        testeditU = app.test_client(self)
        testeditU.post('/login', data=dict(username="Toby", password="Toby"))
        res = testeditU.post('/users/edit/' + str(UserManagementTest.testUid), data=dict(username="testEdit",
                                                                                         password="testEdit123",
                                                                                         type="user",
                                                                                         email="testEdit@gmail.com"))
        dbRes = str(fetchAllUsers())
        self.assertIn("testEdit", dbRes)
        self.assertIn("testEdit@gmail.com", dbRes)

    def test_4_deleteUser(self):
        testdeleteU = app.test_client(self)
        testdeleteU.post('/login', data=dict(username="Toby", password="Toby"))
        res = testdeleteU.get(('/users/delete/' + str(UserManagementTest.testUid)))
        dbRes = str(fetchAllUsers())
        self.assertNotIn(str(UserManagementTest.testUid), dbRes)
