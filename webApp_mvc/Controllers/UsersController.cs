using Microsoft.AspNetCore.Mvc;
using webApp_mvc.Models;  // Adjust namespace as needed for your project
using MongoDB.Driver;
using System.Threading.Tasks;
using MongoDB.Bson.Serialization.Attributes;
using MongoDB.Bson;

public class UserController : Controller
{
    private readonly MongoDBService _mongoDBService;
    private readonly IMongoCollection<User> _usersCollection;

    public UserController(MongoDBService mongoDBService)
    {
        _mongoDBService = mongoDBService;
        _usersCollection = _mongoDBService.GetCollection<User>("Users");
    }

    // GET: /User/Profile
    public async Task<IActionResult> Profile(string id)
    {
        if (string.IsNullOrEmpty(id))
        {
            return BadRequest("User ID is required.");
        }

        if (!ObjectId.TryParse(id, out ObjectId objectId))
        {
            return BadRequest("Invalid User ID format.");
        }

        var user = await _usersCollection.Find(u => u._id == objectId).FirstOrDefaultAsync();
        if (user == null)
        {
            return NotFound($"User not found. Received ID: {id}, Converted ID: {objectId}");
        }

        return View(user);
    }
    public async Task<IActionResult> Index()
    {
        var users = await _usersCollection.Find(_ => true).ToListAsync(); 
        return View(users); 
    }


}



public class User
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public ObjectId _id { get; set; }
    public string Username { get; set; }
    public string Name { get; set; }
    public int Age { get; set; }
    public string Gender { get; set; }
    public string Contact { get; set; }
    public string Description { get; set; }
    public string Photo { get; set; }
}

