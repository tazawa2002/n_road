import threading
from time import sleep
import random

from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
from mcpi.block import *

class n_road():
    # 初期化メソッド
    def __init__(self, n):
        self.ad = "192.168.1.174"
        self.mc = Minecraft.create(address=self.ad)
        self.origin = Vec3(0,0,0)
        self.t1 = threading.Thread(target=self.thread1)
        self.score = 0
        self.n = n
        self.state = 0
        self.anomaly_number = 5
        print("initialize n_load")

    # ゲームを実行するメソッド
    def Run(self):
        self.seiti()
        self.set_field()
        self.makeRoad(0)
        self.mc.player.setTilePos(self.origin+Vec3(3,1,-2))
        self.t1.start()
        self.t1.join()

    # setBlocks()のオーバーラップ
    def setBlocks(self, pos1, pos2, block):
        self.mc.setBlocks(self.origin+pos1, self.origin+pos2, block)

    def setTilePos(self, pos):
        self.mc.player.setTilePos(self.origin + pos)
    
    def getTilePos(self):
        return self.mc.player.getTilePos() + self.origin
    
    # setBlock()のオーバーラップ
    def setBlock(self, pos, block):
        self.mc.setBlock(self.origin+pos, block)

    def seiti(self):
        # 整地
        self.setBlocks(Vec3(-50,0,-50),Vec3(50,50,50),AIR)
        self.setBlocks(Vec3(-50,-1,-50),Vec3(50,-1,50),GRASS)

    # フィールドをセットするメソッド
    def set_field(self):

        # 床の設置
        self.setBlocks(Vec3(0,0,0), Vec3(5,0,25), STONE_SLAB) # メイン通路
        self.setBlocks(Vec3(-10,0,-4), Vec3(5,0,-1), STONE_SLAB) # A
        self.setBlocks(Vec3(-16,0,-14), Vec3(-11,0,-1), STONE_SLAB) # A終端
        self.setBlocks(Vec3(0,0,25), Vec3(15,0,28), STONE_SLAB) # B
        self.setBlocks(Vec3(16,0,25), Vec3(21,0,38), STONE_SLAB) # B終端

        # 点字ブロック
        tenji_block_id = STONE_SLAB.withData(1)
        self.setBlocks(Vec3(2,0,0), Vec3(3,0,25), tenji_block_id) # メイン通路
        self.setBlocks(Vec3(-10,0,-3), Vec3(3,0,-2), tenji_block_id) # A
        self.setBlocks(Vec3(2,0,-1), Vec3(3,0,-1), tenji_block_id) # メイン通路 to A
        self.setBlocks(Vec3(-14,0,-14), Vec3(-13,0,-2), tenji_block_id) # A終端
        self.setBlocks(Vec3(-12,0,-3), Vec3(-11,0,-2), tenji_block_id) # A to A終端
        self.setBlocks(Vec3(2,0,26), Vec3(15,0,27), tenji_block_id) # B
        self.setBlocks(Vec3(16,0,26), Vec3(17,0,27), tenji_block_id) # B to B終端
        self.setBlocks(Vec3(18,0,26), Vec3(19,0,38), tenji_block_id) # B終端

        height = 5
        # 天井の設置
        # block_ceiling = AIR
        # block_ceiling = STONE_SLAB
        block_ceiling = GLOWSTONE_BLOCK
        self.setBlocks(Vec3(0,height,0), Vec3(5,height,25), block_ceiling) # メイン通路
        self.setBlocks(Vec3(-10,height,-4), Vec3(5,height,-1), block_ceiling) # A
        self.setBlocks(Vec3(-16,height,-14), Vec3(-11,height,-1), block_ceiling) # A終端
        self.setBlocks(Vec3(0,height,25), Vec3(15,height,28), block_ceiling) # B
        self.setBlocks(Vec3(16,height,25), Vec3(21,height,38), block_ceiling) # B終端

        # 壁の設置
        self.setBlocks(Vec3(-1,0,0), Vec3(-1,height,29), STONE_SLAB_DOUBLE)
        self.setBlocks(Vec3(0,0,29), Vec3(15,height,29), STONE_SLAB_DOUBLE)
        self.setBlocks(Vec3(15,0,29), Vec3(15,height,39), STONE_SLAB_DOUBLE)
        self.setBlocks(Vec3(16,0,39), Vec3(22,height,39), STONE_SLAB_DOUBLE)
        self.setBlocks(Vec3(22,0,39), Vec3(22,height,24), STONE_SLAB_DOUBLE)
        self.setBlocks(Vec3(21,0,24), Vec3(6,height,24), STONE_SLAB_DOUBLE)
        self.setBlocks(Vec3(6,0,23), Vec3(6,height,-5), STONE_SLAB_DOUBLE)
        self.setBlocks(Vec3(5,0,-5), Vec3(-10,height,-5), STONE_SLAB_DOUBLE)
        self.setBlocks(Vec3(-10,0,-6), Vec3(-10,height,-15), STONE_SLAB_DOUBLE)
        self.setBlocks(Vec3(-11,0,-15), Vec3(-17,height,-15), STONE_SLAB_DOUBLE)
        self.setBlocks(Vec3(-17,0,-14), Vec3(-17,height,0), STONE_SLAB_DOUBLE)
        self.setBlocks(Vec3(-17,0,0), Vec3(-1,height,0), STONE_SLAB_DOUBLE)
        
        # 中の空間を綺麗にする。
        self.setBlocks(Vec3(0,1,-4), Vec3(5,4,28), AIR)
        self.setBlocks(Vec3(6,1,25), Vec3(16,1,28), AIR)
        self.setBlocks(Vec3(-10,1,-4), Vec3(-1,1,-1), AIR)
    
    # プレイヤーの位置を監視するスレッド
    def thread1(self):
        while True:
            pos = self.getTilePos()
            if self.score == self.n:
                break
            elif pos.x > self.origin.x+10:
                # 異変判定
                judge = self.judgement(0)
                if judge == True:
                    self.score += 1
                else :
                    self.score = 0
                self.mc.postToChat(self.score)

                # 通路作り替え
                self.makeRoad(0)

                # テレポート
                self.setTilePos(Vec3(-5, pos.y, pos.z-29))
            elif pos.x < self.origin.x-5:
                # 異変判定
                judge = self.judgement(1)
                if judge == True:
                    self.score += 1
                else :
                    self.score = 0
                self.mc.postToChat(self.score)

                # 通路作り替え
                self.makeRoad(1)

                # テレポート
                self.setTilePos(Vec3(10, pos.y, pos.z+29))
            sleep(0.5)
        
        # 8番出口の時の処理
        self.set_field()
        if self.state == 0:
            pass
        else:
            pass

    def judgement(self, val):
        ans = False
        if val == self.state:
            ans = True
        return ans
    
    def makeRoad(self, val):
        random_val = random.randrange(10)
        self.state = self.__random_func(val, random_val)
        self.set_field()
        self.setBlocks(Vec3(0,1,-4), Vec3(5,4,28), AIR)
        self.setBlocks(Vec3(6,1,25), Vec3(16,1,28), AIR)
        self.setBlocks(Vec3(-10,1,-4), Vec3(-1,1,-1), AIR)
        if self.state != val: # 異常の生成
            if random_val == 0:
                if val == 0:
                    self.setBlocks(Vec3(0,1,25), Vec3(5,1,28), WATER)
                else:
                    self.setBlocks(Vec3(0,1,-4), Vec3(5,1,-1), WATER)
            elif random_val == 1:
                self.setBlock(Vec3(2,3,12), BEDROCK_INVISIBLE)
                self.setBlock(Vec3(3,3,12), BEDROCK_INVISIBLE)
            elif random_val == 2:
                self.setBlocks(Vec3(0,0,0),Vec3(5,0,24), BEDROCK_INVISIBLE)
            elif random_val == 3:
                if val == 0:
                    self.setBlocks(Vec3(0,1,25), Vec3(5,1,28), LAVA)
                else:
                    self.setBlocks(Vec3(0,1,-4), Vec3(5,1,-1), LAVA)
            else:
                self.setBlock(Vec3(2,1,12), SANDSTONE)
                self.setBlock(Vec3(3,1,12), SANDSTONE)

    
    def __random_func(self, val, random_val):
        if random_val >= self.anomaly_number:
            ans = val
        else :
            if val == 0:
                ans = 1
            else :
                ans = 0
        return ans
        


def main():
    game = n_road(8)
    game.Run()
    game.mc.postToChat("Restart game after 60sec")

if __name__ == "__main__":
    while True:
        main()
        sleep(60)