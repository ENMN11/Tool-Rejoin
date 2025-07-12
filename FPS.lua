task.spawn(function()
	pcall(function()
		local p=game:GetService("Players").LocalPlayer
		local g=Instance.new("ScreenGui",p:WaitForChild("PlayerGui"))
		g.IgnoreGuiInset=true g.DisplayOrder=math.huge g.ResetOnSpawn=false
		local f=Instance.new("Frame",g)
		f.Size=UDim2.new(1,0,1,0) f.BackgroundColor3=Color3.new() f.BorderSizePixel=0
		local l=game:GetService("Lighting") l.Brightness=0
		workspace.CurrentCamera.FieldOfView=1
	end)
end)
