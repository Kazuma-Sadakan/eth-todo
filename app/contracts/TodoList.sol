pragma solidity ^0.8.0;

contract TodoList{
    uint public taskCount = 0;

    struct Task{
        uint id;
        string task;
        bool completed;
    }

    mapping (uint => Task) public tasks;

    event TaskCreated(
        uint id,
        string content,
        bool completed
    );

    event TaskCompleted(
        uint id,
        bool completed
    );

    constructor() public {
        createTask("Use the todo list");
    }

    function createTask(string memory _content) public {
        taskCount ++;
        tasks[taskCount] = Task({id: taskCount, task: _content, completed: false});
        emit TaskCreated({id: taskCount, content: _content, completed: false});
    }

    function completeTask(uint _id) public {
        Task memory _task = tasks[_id];
        _task.completed = true;
        tasks[_id] = _task;
        emit TaskCompleted({id: _id, completed: _task.completed});
    }

}