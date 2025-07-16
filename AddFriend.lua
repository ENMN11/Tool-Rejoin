task.spawn(function()
    local Players = game:GetService("Players")
    local localPlayer = Players.LocalPlayer

    for _, player in ipairs(Players:GetPlayers()) do
        if player ~= localPlayer and not player:IsFriendsWith(localPlayer.UserId) then
            pcall(function()
                localPlayer:RequestFriendship(player)
            end)
            task.wait(1)
        end
    end
end)
