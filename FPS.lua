local p=game:GetService("Players").LocalPlayer
local g=Instance.new("ScreenGui",p:WaitForChild("PlayerGui"))
g.IgnoreGuiInset=true g.DisplayOrder=1/0 g.ResetOnSpawn=false
local f=Instance.new("Frame",g)
f.Size=UDim2.new(1,0,1,0) f.BackgroundColor3=Color3.new() f.BorderSizePixel=0
local l=game:GetService("Lighting") local w=game:GetService("Workspace") local c=w.CurrentCamera
pcall(function()
c.FieldOfView=1
for _,v in ipairs(c:GetChildren())do if v:IsA("PostEffect")then v.Enabled=false end end
l.GlobalShadows=false l.Brightness=0 l.ClockTime=0
l.FogStart=0 l.FogEnd=0.01 l.FogColor=Color3.new()
l.EnvironmentDiffuseScale=0 l.EnvironmentSpecularScale=0 l.OutdoorAmbient=Color3.new()
for _,v in ipairs(l:GetChildren())do if v:IsA("PostEffect")then v.Enabled=false end end
local t=w:FindFirstChildOfClass("Terrain")
if t then t.WaterWaveSize=0 t.WaterWaveSpeed=0 t.WaterTransparency=1 t.WaterReflectance=0 end
end)
