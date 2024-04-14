import discogs_client as dc
import secrettoken as st

d = dc.Client('my_user_agent/1.0', user_token=st.token)

user = d.user("AndrewWaterloo")
print(user)
# print("items in inventory ", inventory.count)

# for x in range(inventory.pages) :
#     print("page %d: \n%s\n" %(x, inventory.page(x)))

